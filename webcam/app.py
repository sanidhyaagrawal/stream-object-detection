import cv2
# import torch
import time
import numpy as np

class Inference:
    def __init__(self) -> None:
        self.model = torch.hub.load(
            'ultralytics/yolov5', 'yolov5s', force_reload=True)
        self.device = torch.device('cpu')

    def predict(self, frame:np.ndarray) -> list:
        """
        Predict the objects in the frame

        input:
            frame: np.ndarray
        output:
            list of objects
        """
        results = self.model(frame, size=640)
        return results.pandas().xyxy[0].to_dict(orient="records")


class AnomalyDetector:
    '''
    Assuming it's anomaly if `person` is detected with confidence is greater than 0.5
    '''

    theshold = 0.5
    def detect(self, results: list) -> bool:
        """
        Detect if the results are anomaly or not

        input:
            results: list of objects
        output: 
            True if it's anomaly
        """
        
        for result in results:
            if all([result["confidence"] > self.theshold,
                    result["name"] == "person"]):
                print("Anomaly detected")
                # we can make an api call here to send a notification
                return True
        return False


class WebCam:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        self.frame = None

    def get_frame(self):
        """
        Get the frame from the webcam
        """
        ret, frame = self.cap.read()
        self.frame = frame
        return frame

    def close(self):
        """
        Close the webcam
        """
        self.cap.release()


if __name__ == "__main__":
    # inference = Inference()
    anomaly = AnomalyDetector()
    while True: # Keep retrying to connect to the camera every 5 seconds
        cam = WebCam()
        while cam.cap.isOpened():
            frame = cam.get_frame()
            # results = inference.predict(frame)
            # anomaly.detect(results)
        cam.close()
        print("Retrying in 5 seconds")
        time.sleep(5)
