from imgurpython import ImgurClient
import os

def init_imgur_client(client_id, client_secret):
    return ImgurClient(client_id, client_secret)

def upload_to_imgur(file_path, imgur_client):
    uploaded_image = imgur_client.upload_from_path(file_path)
    return uploaded_image['link']

if __name__ == '__main__':
    # Replace 'your_client_id' and 'your_client_secret' with your actual Imgur credentials
    client_id = os.getenv('IMGUR_CLIENT_ID', None)
    client_secret = os.getenv('IMGUR_SECRET_KEY', None)
    image_path = 'image_message.jpeg'
    upload_to_imgur(image_path, init_imgur_client(client_id, client_secret))

