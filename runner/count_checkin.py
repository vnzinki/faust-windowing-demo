from datetime import datetime

import faust
from config.env import KAFKA_URI
from entity.auth_user_login import LoginCheckinEvent


def user_continous_checkin_count(key, events):
    print(
        "Reward: {} checkin {} times from {} to {}".format(
            key[0],
            events,
            datetime.fromtimestamp(key[1][0]),
            datetime.fromtimestamp(key[1][1])
        )
    )
    if (events >= 3):
        checkin_reward.send_soon(
            value=LoginCheckinEvent(
                user_id=key[0],
                count=events,
                from_time=key[1][0],
                to_time=key[1][1]))


app = faust.App(
    'checkin_processor',
    broker=KAFKA_URI,
    store="memory://",
    topic_partitions=1,
    broker_max_poll_records=1)

checkin_topic = app.topic('user_checkin', value_type=LoginCheckinEvent, partitions=1)
checkin_reward = app.topic('user_reward', value_type=LoginCheckinEvent, partitions=1)


user_login_checkin_count = app.Table(
    'user_login_checkin_count',
    default=int,
    on_window_close=user_continous_checkin_count).tumbling(
        size=90,
        expires=1,
        key_index=True)


@app.agent(checkin_topic)
async def count_user_login_checkin(login_checkin_events):
    async for login_checkin_event in login_checkin_events:
        key = "user:{}".format(str(login_checkin_event.user_id))
        user_login_checkin_count[key] += 1
        print(
            "{} checkin from {} to {}".format(
                login_checkin_event.user_id,
                datetime.fromtimestamp(login_checkin_event.from_time),
                datetime.fromtimestamp(login_checkin_event.to_time)
            )
        )


if __name__ == '__main__':
    app.main()
