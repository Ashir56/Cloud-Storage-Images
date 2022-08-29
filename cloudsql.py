import psycopg2
from google.cloud import storage
from PIL import Image
import io
import sys
import os

# conn = psycopg2.connect(
#     database="kona-production", user="postgres",
#     password="incloud@2019", host="35.188.112.148")

conn = psycopg2.connect(
    database="kona-db", user="postgres",
    password="incloud@2019", host="35.243.83.15")

client = storage.Client()
# bucket = client.get_bucket('kona-2c5bc.appspot.com')
bucket = client.get_bucket('kona-staging.appspot.com')
db = conn.cursor()


db.execute("SELECT id, avatar from users WHERE avatar IS NOT NULL and avatar <> '';")
records = db.fetchall()
types = ['.jpg', '.jpeg', '.png', '.PNG', '.JPEG', '.JPG']
i = 0
sizes = []
for record in records:
    if record is not None:
        # print(record)
        i += 1
        image = record[1]
        print(image)
        res = any(map(image.__contains__, types))
        if res:
            blob = bucket.get_blob(image)
            size = (blob.size/1024)/1024
            sizes.append(size)
            print(format(size, ".2f"), "MB")
        # bytes = io.BytesIO(content)
        # im = Image.open(bytes)
        #
        # print(im.size)

print("Max size of an image : ", format(max(sizes), ".2f"), "MB")
print("Min size of an image : ", format(min(sizes), ".2f"), "MB")
