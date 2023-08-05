import cv2
import yaml
import os

from ultralytics import YOLO


def predict_img(net_model, filename):
    # mac 调试注释
    current_path = os.path.dirname(__file__)
    model = YOLO(net_model)
    im2 = cv2.imread(filename)
    results = model.predict(source=im2, save=True)
    result_map = {}
    img_list = []
    for r in results:
        data = r.boxes.data
        numpy = data.numpy()
        print(numpy)
        for i in numpy:
            # name = read_coco128_yaml('../datasets/face.yaml', 'names', int(i[5]))
            name = read_coco128_yaml(current_path + '/../datasets/face.yaml', 'names', int(i[5]))
            img_list.append(name)
            result_map = {filename: img_list}
    return result_map


def read_coco128_yaml(filename, key1, key2):
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
        try:
            if key1 in data.keys():
                return data[key1][key2]
            else:
                print(f"{key2} not exist")
        except Exception as e:
            print(f"read_yaml error: {e}")
    return


if __name__ == '__main__':
    result = predict_img('face.pt', 'image/11.jpeg')
    print(result)
