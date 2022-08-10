import torch
from PIL import Image
from io import BytesIO
import base64

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./model_car_type/best.pt')
model.conf = 0.65  # confidence threshold (0-1)
# model.iou = 0.45

to_rus = {'police' :  'Полиция',
          'fire' : 'Пожарная',
          'ambulance' : 'Скорая помощь',
          'other' : 'Обычная',
          'Fuck off' : 'Неудача'}

def detect_car_type(path):
    results = model(path)
    try: 
        res = results.pandas().xyxy[0].iloc[0][6]
    except:
        res = 'Fuck off'
    return to_rus[res]

def show_result(path):
    results = model(path)
    results.render()
    return results.imgs[0]
