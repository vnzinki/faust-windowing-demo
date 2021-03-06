# {
#     "data": {
#         "user_id": "58346",
#         "device": {
#             "created_at": 1647913886263,
#             "updated_at": 1653270662432,
#             "id": "96",
#             "uuid": "b2e64324-9ceb-4e2d-b355-3f4a0651b23b",
#             "device_hash": "b4d13fb1b1fe5648bddc5b72273097c7",
#             "device_info": {
#                 "visitorId": "b4d13fb1b1fe5648bddc5b72273097c7",
#                 "platform": {
#                     "value": "Mac OS",
#                     "duration": 0
#                 },
#                 "browserName": "Chrome",
#                 "browserVersion": "101.0.4951.64",
#                 "timezone": {
#                     "value": "Asia/Saigon",
#                     "duration": 6
#                 },
#                 "screenResolution": {
#                     "value": [
#                         900,
#                         1440
#                     ],
#                     "duration": 0
#                 },
#                 "audio": {
#                     "value": 124.04344968475198,
#                     "duration": 2
#                 }
#             }
#         },
#         "lang": "en",
#         "ip": "18.140.232.78",
#         "is_register": true,
#         "time": 1653270662453
#     },
#     "create_time": 1653270662617,
#     "version": 1
# }

from datetime import datetime

import faust
from faust.models.fields import DatetimeField


def parse_millis(ms):
    return datetime.fromtimestamp(int(ms) / 1000)


class LoginEventData(faust.Record, coerce=True):
    user_id: int
    # device: dict
    # ip: str
    time: datetime = DatetimeField(date_parser=parse_millis)


class LoginEvent(faust.Record):
    data: LoginEventData


class LoginCheckinEvent(faust.Record):
    user_id: int
    count: int
    from_time: int
    to_time: int
