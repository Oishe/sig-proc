# downloads any new csv files
#  creates file:
# - users_raw.json -> with all info from firebase
# - db_files.json -> all sessions sorted by filename

from os import listdir
from os.path import isfile, join
import csv
import json
import pickle
import firebase_admin
from firebase_admin import credentials, firestore, storage


cred = credentials.Certificate(
    "/home/oishe/eeg-wave-firebase-adminsdk-0diq9-ea10a414ec.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
app = firebase_admin.initialize_app (
    cred,
    {'storageBucket': 'eeg-wave.appspot.com'},
    name='storage'
)


bucket = storage.bucket(app=app)

doc_ref = db.collection(u'Users')

# raw database collected from firebase
db_users = dict()

for user_doc in doc_ref.get():
    user = user_doc.to_dict()
    sessions = dict()
    # all session info
    for sess_doc in doc_ref.document(user_doc.id).collection('Sessions').get():
        session = sess_doc.to_dict()
        download_link = user['uid']+"/"+session['fileId']
        blob = bucket.blob(download_link)
        if blob.exists():
            # print(download_link)
            session['download_link'] = download_link
            sessions[session['fileId']] = session
    del user['email']
    del user['photoURL']
    user['sessions'] = sessions
    db_users[user['displayName']] = user


with open('firebase_raw.json', 'w') as fp:
    json.dump(db_users, fp, indent=4)

print('Saving firebase_raw.json')

# database organized by files
# new files are downloaded
db_files = dict()

file_dir = './recordings'
csvfiles = [f for f in listdir(file_dir) if isfile(join(file_dir, f))] 

for user_name, user_data in db_users.items():
    for file_name, file_data in user_data['sessions'].items():
        if not file_name in csvfiles:
            download_link = file_data['download_link']
            print(download_link)
            print('downloading.......')
            with open("./recordings/"+file_name, "wb") as fp:
                blob = bucket.blob(download_link)
                blob.download_to_file(fp)
        file_data['user_name'] = user_name
        del file_data['download_link']
        db_files[file_name] = file_data

with open('db_files.json', 'w') as fp:
    json.dump(db_files, fp, indent=4)

print('Saving db_files.json')


with open('db_files.csv', mode='w') as csv_file:
    fieldnames = ['fileId', 'activity', 'user_name', 'songId', 'startTime', 'activityStartTime',
                  'activityStopTime', 'stopTime']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for key, val in db_files.items():
        writer.writerow(val)

print('Saving db_files.csv')


with open('db_files.pickle', 'wb') as handle:
    pickle.dump(db_files, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Saving db_files.pickle')

print('All csv files updated')
print('done')
