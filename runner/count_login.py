import faust
from config.env import KAFKA_URI
from entity.auth_user_login import LoginEvent

app = faust.App('count_login', broker=KAFKA_URI, store="memory://")
login_topic = app.topic('dev_auth_user_login', value_type=LoginEvent)


@app.agent(login_topic)
async def count_login(login_event):
    async for login_event in login_event:
        print(login_event)
