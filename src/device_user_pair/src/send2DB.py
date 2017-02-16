from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import json
import re

Base = declarative_base()

class UserDeviceMap(Base):

    __tablename__ = 'user_device_map'

    id = Column(Integer, primary_key=True)
    device_id = Column(String)
    user_id = Column(String)
    first_active = Column(DATETIME)
    last_active = Column(DATETIME)

## UserDevicePair = (user_id, device_id)
# def send2DB(UserDevicePair, engine):
#     # Initialize connect:
#     # Create DBSession object:
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     new_mapping = UserDeviceMap(user_id=UserDevicePair[0], device_id=UserDevicePair[1],
#                                 first_active=UserDevicePair[2], last_active=UserDevicePair[3])
#     session.add(new_mapping)
#     session.commit()
#     session.close()
    ##add one week to the record's send_at attribute

def main():
    valid_id = re.compile('[0-9A-Za-z/-]{36,36}|[0-9a-z]{12,16}')

    with open('UserDeviceMap.json', 'r', encoding='utf-8') as f:
        reader = f.readlines()
    f.close()
    mapSet = json.loads(reader[0])

    engine = create_engine('mysql+pymysql://HSDBADMIN:NestiaHSPWD@hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com:3306/notification?charset=utf8mb4')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for device_id in mapSet.keys():
        if valid_id.search(device_id) or device_id == 'None':
            user_id = ','.join(mapSet[device_id][0])
            UserDevicePair = (user_id, device_id, mapSet[device_id][1], mapSet[device_id][2])
            new_mapping = UserDeviceMap(user_id=UserDevicePair[0], device_id=UserDevicePair[1],
                                        first_active=UserDevicePair[2], last_active=UserDevicePair[3])
            session.add(new_mapping)
            session.commit()
            print('Sending successful')
    session.close()

main()

