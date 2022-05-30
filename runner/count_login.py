from datetime import datetime

import faust
from config.env import KAFKA_URI
from entity.auth_user_login import LoginCheckinEvent, LoginEvent


def user_continous_login_count(key, events):
    print(
        "{} login {} times from {} to {}".format(
            key[0], events, datetime.fromtimestamp(
                key[1][0]), datetime.fromtimestamp(
                key[1][1])))

    login_checkin.send_soon(
        value=LoginCheckinEvent(
            user_id=key[0],
            count=events,
            from_time=key[1][0],
            to_time=key[1][1]))


app = faust.App(
    'login_processor',
    broker=KAFKA_URI,
    store="memory://",
    topic_partitions=1,
    broker_max_poll_records=1)

login_topic = app.topic('user_login', value_type=LoginEvent, partitions=1)
login_checkin = app.topic('user_checkin', value_type=LoginCheckinEvent, partitions=1)

user_login_count = app.Table(
    'user_login_count',
    default=int,
    on_window_close=user_continous_login_count).tumbling(
        size=30,
        expires=1).relative_to_field(LoginEvent.data.time)


@app.agent(login_topic)
async def count_user_login(login_events):
    async for login_event in login_events:
        key = "user:{}".format(str(login_event.data.user_id))
        user_login_count[key] += 1
        print("Login User: {} => {}".format(key, user_login_count[key].current()))

if __name__ == '__main__':
    app.main()
