import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
# nomeroff_net_dir = os.path.join(current_dir, "../nomeroff_net/")
# print(nomeroff_net_dir)
# sys.path.append(nomeroff_net_dir)

from nomeroff_net import pipeline
from nomeroff_net.tools import unzip
# import timeit

number_plate_detection_and_reading = pipeline("number_plate_detection_and_reading", image_loader="opencv")

def detect_number(path):

    # start = timeit.default_timer()
    result = number_plate_detection_and_reading([
        os.path.join(current_dir, path),
    ])

    (images, images_bboxs,
        images_points, images_zones, region_ids,
        region_names, count_lines,
        confidences, texts) = unzip(result)

    # (['AC4921CB'], ['RP70012', 'JJF509'])
    # stop = timeit.default_timer()
    # print(texts)
    return texts[0]


# detect_number('Images/60.jpg')