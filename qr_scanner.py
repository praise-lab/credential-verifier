import cv2
from pyzbar.pyzbar import decode

def read_qr(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    decoded_objects = decode(img)

    if decoded_objects:
        qr_data = decoded_objects[0].data.decode("utf-8")
        return qr_data

    return None
