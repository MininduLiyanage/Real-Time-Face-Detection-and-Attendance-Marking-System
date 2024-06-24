import cv2
import face_recognition
import os
import pickle
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

# Importing employee images
folderPath = 'Images'
pathList = os.listdir(folderPath)
# print(pathList)

imgList = []
employeeIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))  #collect employee imgs
    employeeIds.append(os.path.splitext(path)[0])                #collect employee ids

    fileName = f'{folderPath}/{path}'
    # print(employeeIds)
    # print(imgList)
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

def findEncodings(imagesList):
    '''
    Encode faces of employees
    '''
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, employeeIds]
print("Encoding Completed")
# print(len(encodeListKnown[0]))   #128

file = open("EncodeFile.p", 'wb')  #pickle file
pickle.dump(encodeListKnownWithIds, file)
file.close()