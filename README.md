Overspeed Vehicle Detection System

An AI-based system that detects vehicles from video, estimates their
speed, and flags overspeeding vehicles using computer vision and deep
learning.

Project Overview

-   Detect vehicles in traffic video
-   Estimate speed using frame-based motion
-   Flag overspeeding vehicles
-   Provide web interface for upload and results

Tech Stack

Python, OpenCV, YOLOv8, PyTorch, Flask, NumPy

System Workflow

Upload Video → Frame Processing → Vehicle Detection → Speed Estimation →
Overspeed Detection → Output Video

Model

-   YOLOv8 (Nano)
-   Real-time object detection
-   Efficient and lightweight

Detection Classes

-   Car
-   Motorcycle
-   Bus
-   Truck

Speed Estimation

Speed = Distance / Time
Scaled: speed = (distance_pixels / time_taken) * 0.1

Tracking

Simple ID assignment using bounding box center: obj_id = int(cx / 100)

Features

-   Bounding boxes on vehicles
-   Overspeed alerts
-   Processed video output

Project Structure

vehicle_violation_project/ - app.py - vehicle.py - templates/ -
uploads/ - outputs/ - requirements.txt

Setup Instructions

1.  Clone repo
2.  Create virtual environment
3.  Install dependencies
4.  Run app.py
5.  Open browser at http://127.0.0.1:5000

Limitations

-   Not real-world calibrated
-   Basic tracking
-   No number plate detection
-   Not fully real-time

Conclusion

A functional prototype combining deep learning, computer vision, and web
deployment for traffic monitoring.
