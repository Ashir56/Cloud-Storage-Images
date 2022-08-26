import psycopg2
from google.cloud import storage
from PIL import Image
import io
import sys
import os


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'w') as file:
        file.write(data)

conn = psycopg2.connect(
    database="kona-db", user="postgres",
    password="incloud@2019", host="35.243.83.15")

client = storage.Client()
bucket = client.get_bucket('kona-staging.appspot.com')
db = conn.cursor()
db.execute("SELECT file from space_images WHERE file IS NOT NULL and file <> '';")
records = db.fetchall()
i = 0
sizes = []
for record in records:
    if record is not None:
        i += 1
        image = record[0]
        print(image)
        if ('.jpg' in image or '.png' in image) or ('.JPEG' in image or '.PNG' in image):
            blob = bucket.get_blob(image)
            content = blob.download_as_string()
            sizes.append((content.__sizeof__() /1024)/1024)
            print(sizes)
        # bytes = io.BytesIO(content)
        # im = Image.open(bytes)
        #
        # print(im.size)

print("Max size of an image : ", format(max(sizes), ".2f"), "MB")
print("Min size of an image : ", format(min(sizes), ".2f"), "MB")
