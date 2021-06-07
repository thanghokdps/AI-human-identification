from datetime import datetime
import pyrebase


firebaseConfig = {
    "apiKey": "AIzaSyBPnOpRicmohEw0jUrxHeZzcPciL9PrxBA",
    "authDomain": "pbl5-c18f5.firebaseapp.com",
    "databaseURL": "https://pbl5-c18f5-default-rtdb.firebaseio.com",
    "projectId": "pbl5-c18f5",
    "storageBucket": "pbl5-c18f5.appspot.com",
    "messagingSenderId": "679297861153",
    "appId": "1:679297861153:web:8af51e474125ecde0dc560",
    "measurementId": "G-TSTJZGWMS1"
  }
firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
storage = firebase.storage()
now = datetime.now()
datetime_now = now.strftime("%Y-%m-%d %H:%M")
date_now = now.strftime("%Y-%m-%d")

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)

def LightStatus(status):
    data = {
        'id_account': 1,
        'status': status,
        'time': datetime_now
    }
    db.child('Light').push(data)

def addImage():
    # if storage.child("Image")!=None:
    #     storage.delete("Image")
    storage.child("Image").put("object-detection.jpg")
def Consumption(total):
    temp = db.child('Consumption').get()
    for i in temp.each():
        if i.val()['day']==date_now:
            db.child('Consumption').child(i.key()).update({"total":i.val()['total']+total})
            return
    data = {
            'id_account': 1,
            'day': date_now,
            'total': total
    }
    db.child('Consumption').push(data)