import cv2
import os
import numpy as np
import pickle
import face_recognition
import cvzone

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-recognizer-acc6a-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': "face-recognizer-acc6a.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture('web4.mp4')
# cap.set(3, 640)
# cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)

imgList = []

for path in modePathList:
    imgList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgList))


# Load the encoding file
file = open('StudentEncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, employeeIds = encodeListKnownWithIds
# print(encodeListKnown)

modeType = 0  #related to modes of visuals
counter = 0
id = -1
imgEmployee = []


while True:
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):  # current frame = total frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # reset video to initial frame - loop the video
    # print(success)
    img = cv2.resize(img, (640, 480))

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 630, 808:808 + 414] = imgList[modeType]

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # reduce the image size
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)                  # find faces in current frame
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)  # find encodings by giving locations of face
    #print(encodeCurFrame)

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  # compare similarity
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  # lower the distance better the match
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                id = employeeIds[matchIndex]
                # print(id)

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4     # because we scaled by 0.25
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1          # adjusting according to the bg frame
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Detecing", (275, 400))
                    #cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

    if counter != 0:

        if counter == 1:

            employeeInfo = db.reference(f'Employees/{id}').get()      # Get the Data
            print(employeeInfo)

            blob = bucket.get_blob(f'Images/{id}.jpg')              # Get the Image from the storage
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgEmployee = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

            # Update data of attendance
            datetimeObject = datetime.strptime(employeeInfo['last_attendance_time'],
                                               "%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
            print(secondsElapsed)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            if secondsElapsed > 30:      #here time duration between 2 attendance marking of the same person is set to 30 seconds for testing purposes
                ref = db.reference(f'Employees/{id}')
                employeeInfo['total_attendance'] += 1
                ref.child('total_attendance').set(employeeInfo['total_attendance'])         # update database
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                modeType = 3
                counter = 0
                imgBackground[44:44 + 630, 808:808 + 414] = imgList[modeType]

        if modeType != 3:

            if 10 < counter < 20:
                modeType = 2

            imgBackground[44:44 + 630, 808:808 + 414] = imgList[modeType]

            if counter <= 10:
                cv2.putText(imgBackground, str(employeeInfo['total_attendance']), (861, 125),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
                cv2.putText(imgBackground, str(employeeInfo['Department']), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(employeeInfo['Position']), (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                # cv2.putText(imgBackground, str(employeeInfo['year']), (1025, 625),
                #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(employeeInfo['starting_year']), (1125, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                (w, h), _ = cv2.getTextSize(employeeInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)  # center employee name
                offset = (414 - w) // 2
                cv2.putText(imgBackground, str(employeeInfo['name']), (808 + offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                imgBackground[175:175 + 216, 909:909 + 216] = imgEmployee

            counter += 1

            if counter >= 20:
                counter = 0
                modeType = 0
                studentInfo = []
                imgStudent = []
                imgBackground[44:44 + 630, 808:808 + 414] = imgList[modeType]

    else:
        modeType = 0
        counter = 0


    # cv2.imshow("Webcam", img)
    cv2.imshow("Face", imgBackground)
    cv2.waitKey(1)


#https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78