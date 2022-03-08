# import required libraries
from vidgear.gears import NetGear
import cv2
import time
import numpy as np
import torch
import sys

options = {"bidirectional_mode": True,
            "max_retries": 500
            }


class Inference:
    def __init__(self) -> None:
        self.model = torch.hub.load(
            'ultralytics/yolov5', 'yolov5s', force_reload=True)
        self.device = torch.device('cpu')
        self.model.conf = 0.4

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

    theshold = 0.3
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
                # print("Anomaly detected")
                # we can make an api call here to send a notification
                return True
        return False

class Stream:
    def __init__(self) -> None:
        self.client = NetGear(receive_mode=True, **options)
    
    def get_frame(self, target_data: dict= None) -> np.ndarray:
        """
        Get the frame from the server
        """
        _, frame = self.client.recv(return_data=target_data)
        return frame
    
    def close(self):
        """
        Close the server
        """
        self.client.close()

if __name__ == "__main__":
    inference = Inference()
    anomaly = AnomalyDetector()

    while True: # Keep retrying to connect to the stream every 5 seconds
        try:
            stream = Stream()
            frame = stream.get_frame()
            while len(frame) != 0:
                results = inference.predict(frame)
                # print(results)
                is_anomal = anomaly.detect(results)
                frame = stream.get_frame({'results': results, 'is_anomal': is_anomal})
                print("Recived frame of size {}".format(sys.getsizeof(frame)))
        except Exception as e:
            print("Retrying in 2 seconds")
            time.sleep(2)
        finally:
            stream.close()
      

