# Real-Time-Face-Detection-and-Attendance-Marking-System
This project is designed to be a real-time face detection and attendance marking system, ideal for use at the corporate level. By leveraging computer vision techniques, this system accurately detects and identifies employees, updates their attendance in real-time using Firebase, and provides a streamlined and automated solution for managing attendance records.

## Features
  1. **Face Detection and Recognition**: Utilizes computer vision to detect and identify employees' faces.
  2. **Real-Time Database Integration**: Uses Firebase to store and update attendance data instantly.
  3. **Employee Information Storage**: Maintains comprehensive records of each employee, including ID photos and personal details.
  4. **Repeated Attendance Check**: Prevents duplicate attendance records by recognizing previously marked employees within a configurable time window (e.g., 18 hours).
  5. **Detailed Process Overview**: Updates attendance in real-time upon face detection and displays employee information dynamically.
## Project Overview
## Main Components
  1. **Face Recognition**: Implemented using the face_recognition library to encode and compare facial features. Each face is represented by 128 unique measurements for precise identification.
  2. **Real-Time Attendance** Marking: When an employee's face is detected, the system updates their attendance time in Firebase in real-time and displays the employee's details instantly.
  3. **Duplicate Detection**: After an employee's attendance is marked, the system prevents re-marking within a preset period to avoid duplication.
## File Descriptions
  1. **main.py**: Executes the face detection and attendance marking system. This is the core script that integrates all functionalities and handles real-time operations.
  2. **database_update.py**: Responsible for uploading and updating employee data in Firebase, including details such as employee ID, department, and position.
  3. **encode_generator.py**: Initially encodes the faces of employees to generate a set of unique facial measurements, which are used later for comparison and recognition.
## Libraries Used
  1. **OpenCV**: For capturing and processing video frames.
  2. **face_recognition**: For encoding and recognizing faces.
  3. **Pickle**: For saving and loading encoded face data.
  4. **Datetime**: For handling date and time operations.
  5. **CvZone**: For simplifying some common computer vision tasks.
  6. **firebase_admin**: For integrating and interacting with Firebase services.
## How It Works
  1. **Face Detection**: The system captures live video feed and detects faces in real-time using OpenCV.
  2. **Face Recognition**: Detected faces are encoded and compared against a pre-stored database of employee faces.
  3. **Attendance Marking**: Once an employee's face is recognized, the system updates their attendance in Firebase and displays their details on the screen.
  4. **Duplicate Check**: If the same face is detected again within the preset time window, the system identifies it as already marked and prevents duplicate attendance.
