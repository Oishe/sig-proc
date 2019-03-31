import csv
import json
from collections import namedtuple

# TODO: fileID -> :
# "activity": "Music",
# "fileId": "1553041309127_recording.csv",
# "stopTime": 1553041308703,
# "activityStopTime": 1553041278725,
# "songId": 5,
# "startTime": 1553041029701,
# "activityStartTime": 1553041060725
# "displayName": "Oishe Farhan",
# "uid": "y1WX6WYyw1Q0FLxSar1OIM0HV833",

with open("users.json", 'r') as fp:
    # print(''.join(fp.readlines()))
    data = json.load(fp)
    # print(data)

db_fileId = dict()

for user in data:
    for fid in data[user]['sessions']:
        one_fileId = data[user]['sessions'][fid]
        one_fileId['uid'] = data[user]['uid']
        one_fileId['displayName'] = data[user]['displayName']
        db_fileId[fid] = one_fileId


with open('db_fileID.csv', mode='w') as csv_file:
    fieldnames = ['fileId', 'activity', 'displayName', 'uid', 'songId', 'startTime', 'activityStartTime',
                  'activityStopTime', 'stopTime']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for key, val in db_fileId.items():
        writer.writerow(val)

print('done')
