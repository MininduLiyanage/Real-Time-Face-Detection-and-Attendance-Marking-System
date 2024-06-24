import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://face-recognizer-acc6a-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('Employees')

data = {
    "321654":
        {
            "name": "Chris Evans",
            "Department": "Res & Dev",
            "Position": "Engineer",
            "starting_year": 2022,
            "total_attendance": 72,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Scarlett Johansson",
            "Department": "HR",
            "Position": "Specialist",
            "starting_year": 2023,
            "total_attendance": 45,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Clint Barton",
            "Department": "Finance",
            "Position": "Manager",
            "starting_year": 2019,
            "total_attendance": 70,
            "last_attendance_time": "2023-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)