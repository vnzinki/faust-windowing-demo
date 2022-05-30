import time
from datetime import datetime

import faust
from config.env import KAFKA_URI


class LoginEventData(faust.Record, coerce=True):
    user_id: int
    # device: dict
    # ip: str
    time: int


class LoginEvent(faust.Record):
    data: LoginEventData


app = faust.App(
    'login_processor',
    broker=KAFKA_URI,
    web_enabled=False,
    web_port=7002,
    store="memory://",
    consumer_auto_offset_reset="earliest",
    broker_max_poll_records=1)


login_topic = app.topic(
    'user_login_test',
    value_type=LoginEvent,
)


@app.timer(1)
async def produce():
    data = dict(
        user_id=2,
        time=time.time() * 1000,
    )
    event = LoginEvent(
        data=data
    )
    await login_topic.send(value=event)
    print("publish event: user:{}, time:{}".format(data['user_id'], datetime.fromtimestamp(data['time'] / 1000)))


if __name__ == '__main__':
    app.main()
