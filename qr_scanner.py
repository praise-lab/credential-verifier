
import cv2

def read_qr(file_path):
    img = cv2.imread(file_path)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    return data
