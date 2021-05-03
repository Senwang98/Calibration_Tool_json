import json
import math

import cv2

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def extract_from_json(path, number):
    tmp = path.split('/')
    json_address = tmp[0] + '/json/' + tmp[1] + '/' + str(number) + '_keypoints.json'
    img_address = path + '/kinect_color/' + str(number) + '.jpg'
    img = cv2.imread(img_address)

    # print(json_address)
    with open(json_address, 'r') as f:
        json_tmp = json.load(f)
        people = json_tmp['people']
        for i in range(len(people)):
            face = people[i]['face_keypoints_2d']
            for j in range(0, len(face), 3):
                cv2.circle(img, (int(face[j]), int(face[j + 1])), 3, green, -1)
            img = cv2.putText(img, str(i), (round(face[51]), round(face[52]) - 10), cv2.FONT_HERSHEY_PLAIN, 6, blue, 2)

    return img


def extract_point_from_json(path, number, body_index):
    if body_index == -1:
        return -100
    tmp = path.split('/')
    json_address = tmp[0] + '/json/' + tmp[1] + '/' + str(number) + '_keypoints.json'

    # print(json_address)
    with open(json_address, 'r') as f:
        json_tmp = json.load(f)
        people = json_tmp['people']
        for i in range(len(people)):
            if i == body_index:
                face = people[i]['face_keypoints_2d']
                x1 = face[111]
                y1 = face[112]
                x2 = face[123]
                y2 = face[124]
                dis = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
                break
    return dis


if __name__ == '__main__':
    # img = extract_from_json('Y:/id_19530419_20190801084849/facial_expression', 1)
    # cv2.imshow('line', img)
    # cv2.waitKey(0)
    print(extract_point_from_json('Y:/id_19530419_20190801084849/facial_expression', 1, 1))
