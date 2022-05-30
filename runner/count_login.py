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


def user_continous_checkin_count(key, events):
    print(
        "{} checkin {} times from {} to {}".format(
            key[0], events, datetime.fromtimestamp(
                key[1][0]), datetime.fromtimestamp(
                key[1][1])))
    if (events >= 3):
        checkin_reward.send_soon(
            value=LoginCheckinEvent(
                user_id=key[0],
                count=events,
                from_time=key[1][0],
                to_time=key[1][1]))


app = faust.App(
    'login_processor',
    broker=KAFKA_URI,
    web_port=7001,
    store="memory://",
    consumer_auto_offset_reset="earliest",
    broker_max_poll_records=1)

login_topic = app.topic('user_login_test', value_type=LoginEvent)
login_checkin = app.topic('user_login_checkin', value_type=LoginCheckinEvent)
checkin_reward = app.topic('checkin_reward', value_type=LoginCheckinEvent)

user_login_count = app.Table(
    'user_login_count',
    default=int,
    on_window_close=user_continous_login_count).tumbling(
        size=60,
        expires=1,
        key_index=True).relative_to_field(LoginEvent.data.time)


user_login_checkin_count = app.Table(
    'user_login_checkin_count',
    default=int,
    on_window_close=user_continous_checkin_count).tumbling(
        size=180,
        expires=1,
        key_index=True)


@ app.agent(login_topic)
async def count_user_login(login_events):
    async for login_event in login_events:
        key = "user:{}".format(str(login_event.data.user_id))
        user_login_count[key] += 1
        print("Login User: {} => {}".format(key, user_login_count[key].current()))


@ app.agent(login_checkin)
async def count_user_login_checkin(login_checkin_events):
    async for login_checkin_event in login_checkin_events:
        key = "user:{}".format(str(login_checkin_event.user_id))
        user_login_checkin_count[key] += 1
        print("Checkin User: {} => {}".format(login_checkin_event.user_id, login_checkin_event.count))


if __name__ == '__main__':
    app.main()
