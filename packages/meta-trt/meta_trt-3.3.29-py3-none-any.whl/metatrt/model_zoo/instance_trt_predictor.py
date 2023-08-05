import cv2
import numpy as np
from ..utils import preproc, multiclass_nms, singleclass_nms, sigmoid, fast_dot
from ..utils import BaseEngine
import pycuda.driver as cuda


class InstanceTrtPredictor(BaseEngine):
    def __init__(self, trt_file, image_size=(640, 640)):
        super(InstanceTrtPredictor, self).__init__(trt_file)
        self.image_size = image_size  # (h, w)
        self.mean = None
        self.std = None

    @staticmethod
    def get_rect(mask):
        h, w = mask.shape[:2]
        _, pred = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) < 1:
            return [[0, 0], [0, w - 1], [h - 1, w - 1], [h - 1, 0]]

        area = [cv2.contourArea(c) for c in contours]
        max_idx = np.argmax(area)
        min_rect = cv2.minAreaRect(contours[max_idx])
        min_rect = cv2.boxPoints(min_rect)

        return min_rect

    def predict(self, origin_img, class_names, use_preprocess, conf, iou, use_mask=False, use_cupy=False,
                multi_label=False):
        dets = []
        img, ratio = preproc(origin_img, self.image_size, self.mean, self.std) if use_preprocess else (origin_img, 1.0)
        data = self.infer(img)
        data = [np.ascontiguousarray(x, dtype=np.float64) for x in data]
        # 处理box
        mi = 5 + len(class_names)
        pred = np.reshape(data[-1], (1, -1, mi + 32))[0]
        boxes = self.postprocess(pred, ratio=1., score_thr=conf, nms_thr=iou, multi_label=multi_label)
        if boxes is None: return dets
        # 处理mask
        if use_mask:
            if use_cupy:
                import cupy as cp

                ctx = cuda.Device(0).retain_primary_context()
                ctx.push()
                gpu_data0 = cp.asarray(data[0])
                gpu_proto = cp.reshape(gpu_data0, (1, 32, -1))[0]
                gpu_boxes = cp.asarray(boxes[:, 6:])
                gpu_dot = cp.dot(gpu_boxes, gpu_proto)
                gpu_sigmoid_dot = 1 / (1 + cp.exp(-gpu_dot))
                gpu_masks = cp.reshape(gpu_sigmoid_dot, (-1, 160, 160))
                masks = cp.asnumpy(gpu_masks)
                ih, iw = 160 / self.image_size[0], 160 / self.image_size[1]
                ctx.pop()
            else:
                # csl: about 11ms on i7-8700
                proto = np.reshape(data[0], (1, 32, -1))[0]
                masks = np.reshape(sigmoid(fast_dot(boxes[:, 6:], proto)), (-1, 160, 160))
                ih, iw = 160 / self.image_size[0], 160 / self.image_size[1]

            for mask, box, score, label in zip(masks, boxes[:, :4], boxes[:, 4], boxes[:, 5]):
                x1, y1, x2, y2 = box[0] * iw, box[1] * ih, box[2] * iw, box[3] * ih
                crop = mask[int(y1):int(y2) + 1, int(x1):int(x2) + 1] * 255
                min_rect = self.get_rect(crop.astype(np.uint8))
                rect = [[(r[0] + x1) / ih / ratio, (r[1] + y1) / iw / ratio] for r in min_rect]
                dets.append([max(int(rect[0][0]), 0), max(int(rect[0][1]), 0),
                             max(int(rect[1][0]), 0), max(int(rect[1][1]), 0),
                             max(int(rect[2][0]), 0), max(int(rect[2][1]), 0),
                             max(int(rect[3][0]), 0), max(int(rect[3][1]), 0),
                             float(score), int(label)])
        else:
            for box, score, label in zip(boxes[:, :4], boxes[:, 4], boxes[:, 5]):
                x1, y1, x2, y2 = box[0] / ratio, box[1] / ratio, box[2] / ratio, box[3] / ratio
                dets.append([max(int(x1), 0), max(int(y1), 0),
                             max(int(x2), 0), max(int(y1), 0),
                             max(int(x2), 0), max(int(y2), 0),
                             max(int(x1), 0), max(int(y2), 0),
                             float(score), int(label)])

        return dets

    @staticmethod
    def postprocess(predictions, ratio, score_thr, nms_thr, multi_label=False):
        boxes = predictions[:, :4]
        scores = predictions[:, 4:5] * predictions[:, 5:-32]
        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.
        boxes_xyxy /= ratio

        if multi_label:
            dets = multiclass_nms(boxes_xyxy, scores, nms_thr=nms_thr, score_thr=score_thr, predictions=predictions)
        else:
            dets = singleclass_nms(boxes_xyxy, scores, nms_thr=nms_thr, score_thr=score_thr, predictions=predictions)

        return dets
