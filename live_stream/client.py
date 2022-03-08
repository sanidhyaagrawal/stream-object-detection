# import required libraries
from vidgear.gears import VideoGear
from vidgear.gears import NetGear
import time
import cv2
import sys

options = {
    "jpeg_compression": True,
    "jpeg_compression_quality": 50,
    "jpeg_compression_fastdct": True,
    "jpeg_compression_fastupsample": True,
    "bidirectional_mode": True
}

while True:
    # Keep trying to connect to the server until it's successful every 2 seconds
    try:
        stream = VideoGear(source=0).start()  # start video stream
        server = NetGear(**options)  # try connet to server

        while True:
            frame = stream.read()

            if len(frame) != 0:
                # Send current frame and receive data from server for previous frame
                time.sleep(0.2) # send a frame every 0.2 seconds
                recv_data = server.send(frame) 
                print('Recived {} bits'.format(sys.getsizeof(recv_data)))
                if recv_data:
                    for data in recv_data['results']:
                        # Draw bounding box for detected objects
                        cv2.rectangle(frame, 
                                    (int(data['xmin']), int(data['ymin'])), 
                                    (int(data['xmax']), int(data['ymax'])), 
                                    (0, 255, 0), 2)

                        # Draw label for detected objects
                        frame = cv2.putText(frame, 
                                            data['name'], 
                                            (int(data['xmax']), int(data['ymin'])), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 
                                            1, (0, 255, 0), 2)

                    if recv_data['is_anomal']:
                        # Draw label for anomaly
                        frame = cv2.putText(frame, "Anomaly Detected", 
                                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                                            1, (0, 0, 255), 2)

                    cv2.imshow("Stream", frame)
                    key = cv2.waitKey(1) & 0xFF
            else:
                # If there's no frame, close the client and retry
                break
        
        # Close the client and retry
        stream.stop()
        server.close()

    except RuntimeError:
        print("Retrying in 2 seconds")
        time.sleep(2)
  