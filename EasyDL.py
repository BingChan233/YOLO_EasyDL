import requests
import json
import base64
from io import BytesIO


# 输入标签名称,YOLO格式的数据,图片宽高,转换成label对象,放入list中上传
def YOLO2EasyDL(name, x, y, w, h, pixelX, pixelY):
    w = w * pixelX
    h = h * pixelY
    x = x * pixelX
    y = y * pixelY
    left = x - w // 2
    top = y - h // 2
    return {
        'label_name': name,
        'left': left,
        'top': top,
        'width': w,
        'height': h
    }


# 直接输入predict()的result的item,返回可直接上传的labels
def item2labels(item):
    labels = []
    boxes = item.boxes.xywh
    names = item.boxes.cls
    for name, box in zip(names, boxes):
        x, y, w, h = box
        x, y, w, h = x.item(), y.item(), w.item(), h.item()
        left = x - w // 2
        top = y - h // 2
        name = str(int(name.item()))
        labels.append(
            {
                'label_name': name,
                'left': left,
                'top': top,
                'width': w,
                'height': h
            }
        )
    return labels


class EasyDL:
    def __init__(self, accessToken):
        self.accessToken = accessToken

    def getList(self):
        url = "https://aip.baidubce.com/rpc/2.0/easydl/dataset/list?access_token=" + self.accessToken
        headers = {
            'Content-Type': 'application/json',
        }
        body = {
            'type': "OBJECT_DETECTION",
        }
        body = json.dumps(body)
        response = requests.post(url, headers=headers, data=body)

        print(response.text)

    # 上传PIL图片,labels为list格式,元素为json格式
    def upload_fromPIL(self, dataset_id, img, name, labels=None):
        url = "https://aip.baidubce.com/rpc/2.0/easydl/dataset/addentity?access_token=" + self.accessToken
        img_buffer = BytesIO()
        img.save(img_buffer, format='JPEG')
        byte_data = img_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        base64_str = str(base64_str, 'utf-8')

        headers = {
            'Content-Type': 'application/json',
        }
        if labels is not None:
            body = {
                'type': 'OBJECT_DETECTION',
                'dataset_id': dataset_id,
                'entity_content': base64_str,
                'entity_name': name,
                'labels': labels
            }
        else:
            body = {
                'type': 'OBJECT_DETECTION',
                'dataset_id': dataset_id,
                'entity_content': base64_str,
                'entity_name': name,
            }
        body = json.dumps(body)
        response = requests.post(url, headers=headers, data=body)

        print(response.text)
