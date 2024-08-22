from imgurpython import ImgurClient
import os
from pprint import pprint

client_id = os.getenv('IMGUR_CLIENT_ID', None)
client_secret = os.getenv('IMGUR_SECRET_KEY', None)
image_path = "image_message.jpeg"

client = ImgurClient(client_id, client_secret)
response = client.upload_from_path(image_path)

print(response['link'])