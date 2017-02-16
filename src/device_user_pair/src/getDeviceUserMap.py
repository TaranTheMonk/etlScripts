import json
import time
from datetime import datetime

def TimeTransform():
    return

def oneMoreDay(previousDay):
    previousValue = time.mktime(time.strptime(previousDay, "%Y-%m-%d"))
    previousValue += 24*60*60
    Future = datetime.strftime(datetime.fromtimestamp(previousValue), "%Y-%m-%d")
    return Future

def miningRawLog(path, dictionary):
    with open(path, 'r', encoding='utf-8') as f:
        reader = f.readlines()
    f.close()
    for record in reader:
        row = record.split(',')
        dateString = row[0] + 'T' + row[1]
        ##row = [YMD, HMS, Pair]
        for symbol in ['(', ')', ';']:
            row[2] = row[2].replace(symbol, ',')
        row[2] = row[2].split(',')
        ##row[2] = [user_id, account_name, device_id]
        if row[2][0] == '-':
            row[2][0] = 'None'
        if not row[2][2] in dictionary:
            if row[2][2] != '' and row[2][2] != '\n':
                dictionary.update({row[2][2]: [set(), dateString, dateString]})
            else:
                dictionary['None'][0].add(row[2][0])
        if row[2][2] != '' and row[2][2] != '\n':
            dictionary[row[2][2]][0].add(row[2][0])
            dictionary[row[2][2]][2] = dateString
        else:
            dictionary['None'][0].add(row[2][0])

def miningForDates(startDate, stopDate):
    output_dict = dict()
    output_dict.update({'None': [set(), '', '']})
    currentDate = startDate
    while currentDate != stopDate:
        path = '/device_user_pair/device_id_pair-' + currentDate + '.log'
        miningRawLog(path, output_dict)
        print(currentDate)
        currentDate = oneMoreDay(currentDate)

    for device_id in output_dict.keys():
        if device_id != 'None':
            if 'None' in output_dict[device_id][0] and len(output_dict[device_id][0]) != 1:
                output_dict[device_id][0].discard('None')
            for user_id in output_dict[device_id][0]:
                output_dict['None'][0].discard(user_id)
            #output_dict[user_id] = list(output_dict[user_id])

    for user_id in output_dict.keys():
        output_dict[user_id][0] = list(output_dict[user_id][0])

    with open('UserDeviceMap.json', 'w') as f:
        json.dump(output_dict, f)
    f.close()
    return output_dict

output = miningForDates('2016-06-23', '2017-02-09')