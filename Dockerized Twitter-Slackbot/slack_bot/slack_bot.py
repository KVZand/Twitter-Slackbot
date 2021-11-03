import requests
from sqlalchemy import create_engine, exc
from sqlalchemy.sql import text
import pandas as pd
import time

time.sleep(10)
webhook_url = "https://xxxx"

uri = 'postgresql:/xxxxx'
engine = create_engine(uri, echo=False)
connection = engine.connect()

query_1 = "SELECT distinct(*) FROM tweets WHERE (sentiment !=1) and (sentiment !0=)"
df_ts = pd.DataFrame(connection.execute(query_1).fetchall())
df_ts = df_ts.to_json()
message = 'xxx'

data = {'text': df_ts}
requests.post(url=webhook_url, json = data)
