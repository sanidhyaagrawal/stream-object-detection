# stream-object-detection

***Listen to webcam feed and perform object detection***

<img src="demo.gif"/>

---

### Getting started:
1. [Overview](#overview)
2. [Installation](#installation)
3. [Methods](#methods)
4. [K8s](#k8s-deployment)
---

## Overview

***An application that uses pre-trained PyTorch model to perform object detection in real-time where the video feed is acquired from webcam, packaged using docker and prepared for deployment on Kubernetes***

The whole process is completes in 2 steps:
1. Frames are received from the webcam.
2. The frames are processed using the pre-trained model ([yolov5s](https://github.com/ultralytics/yolov5/releases))
3. If person is detected with confidence greater than 0.5, we consider it as anomaly and send a notification.

The main files and folders in the directory are:
1. webcam
    - 📑 app.py - contains the APIs.
    - 📑 Dockerfile - used for building the docker image.
    - 📑 requirements.txt - used for installing the dependencies.
2. live_stream
    - 📑 client.py - Client side code to stream the video feed from webcam to the server.
    - 📑 server.py - Server side code to process the frames and send the anomaly notifications.
    - 📑 Dockerfile - used for building the docker image.
    - 📑 requirements.txt - used for installing the dependencies.
---

## Installation
- The Docker image can be built using the following command:
    
    ```
    docker build -t sanidhya7921/stream-object-detection .
    ```

- To test your Docker image locally.:

    ```
    docker run sanidhya7921/stream-object-detection     
    ```
> ℹ : to push your Docker image to Docker Hub, use the following command- <br>
`docker push sanidhya7921/stream-object-detection`
---

## Methods


There are 3 Classes for the company profile:
|Class Name|API|Description|
|-|-|-|
|`WebCam`|`WebCam.get_frame`|Get the frame from the webcam|
|`Inference`|`Inference.predict`|Predict the objects in the frame using yolov5s model |
|`AnomalyDetector`|`AnomalyDetector.detect`|Detect if the results are anomaly or not|

---

## K8s Deployment

Deployment resource: 
``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stream-object-detection
spec:
  selector:
    matchLabels:
      app: stream-object-detection
  replicas: 5
  template:
    metadata:
      labels:
        app: stream-object-detection
    spec:
      containers:
      - name: stream-object-detection
        image: stream-object-detection
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
```
---
Service resource: 
``` yaml
apiVersion: v1
kind: Service
metadata:
  name: stream-object-detection
spec:
  selector:
    app: stream-object-detection
  ports:
  - protocol: "TCP"
    port: 5555
    targetPort: 80
  type: LoadBalancer
```

HPA Resource:
``` yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  creationTimestamp: null
  name: stream-object-detection
spec:
  maxReplicas: 2
  minReplicas: 1
  scaleTargetRef:
	apiVersion: apps/v1
	kind: Deployment
	name: stream-object-detection
  targetCPUUtilizationPercentage: 70
```
ConfigMap resource: <br>
> If we want to use .env.prod the following command can be run in the terminal of lens.

```
Kubectl create configmap <map_name> --from-file=".env.prod"
```
---
