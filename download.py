# creates file: users.json with all info
# stores all csv files in recordings folder
import json
import firebase_admin
from firebase_admin import credentials, firestore, storage


cred = credentials.Certificate(
    "/Users/oishe/eeg-wave-firebase-adminsdk-0diq9-26ffab1869.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
app = firebase_admin.initialize_app(
    cred,
    {'storageBucket': 'eeg-wave.appspot.com'},
    name='storage'
)


bucket = storage.bucket(app=app)

doc_ref = db.collection(u'Users')

users = dict()

for user_doc in doc_ref.get():
    user = user_doc.to_dict()
    sessions = dict()
    # all session info
    for sess_doc in doc_ref.document(user_doc.id).collection('Sessions').get():
        session = sess_doc.to_dict()
        blob = bucket.blob(user['uid']+"/"+session['fileId'])
        if blob.exists():
            sessions[session['fileId']] = session
            with open("./recordings/"+session['fileId'], "wb") as fp:
                blob.download_to_file(fp)
            print(user['uid']+"/"+session['fileId'])
    del user['email']
    del user['photoURL']
    user['sessions'] = sessions
    users[user['displayName']] = user


with open('users.json', 'w') as fp:
    json.dump(users, fp, indent=4)

print("done")
