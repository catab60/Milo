import requests
import json
import base64
import os
import shutil
from PIL  import Image, ImageTk
from io import BytesIO


#SERVER_URL = "http://192.168.0.222:5000/get_posts"

server_ip = "localhost"

FILES_DIRECTORY = "appdata"


if not os.path.exists(FILES_DIRECTORY):
    os.makedirs(FILES_DIRECTORY)

def download_files():
    SERVER_URL = f"http://{server_ip}:5000/get_posts"
    items = {}
    

    try:

        for filename in os.listdir(FILES_DIRECTORY):
            file_path = os.path.join(FILES_DIRECTORY, filename)
            os.remove(file_path)
    except Exception as e:
        print(f"Error clearing files: {e}")

    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()

        data = response.json()


        for json_file in data['json_files']:
            json_file_id = json_file.split('_')[2].split('.')[0]
            json_file_path = os.path.join(FILES_DIRECTORY, json_file)
            with open(json_file_path, 'w') as f:
                json.dump(data['json_files'][json_file], f, indent=4)


            items[json_file_id] = []


            for image_file in data['image_files']:
                if image_file.startswith(f"image_{json_file_id}_"):
                    image_id = image_file.split('_')[-1].split('.')[0]
                    items[json_file_id].append(image_id)

        for image_file, encoded_image in data['image_files'].items():
            image_file_path = os.path.join(FILES_DIRECTORY, image_file)
            with open(image_file_path, 'wb') as f:
                f.write(base64.b64decode(encoded_image))

    except Exception as e:
        print(f"An error occurred: {e}")


    return items


def get_games():
    SERVER_URL = f"http://{server_ip}:5000/get_games"
    response = requests.get(SERVER_URL)
    response.raise_for_status()

    data = response.json()


    class_definitions = data.get("games", [])


    file_path = os.path.join(os.getcwd(), "games.py")


    if os.path.exists(file_path):
        os.remove(file_path)


    with open(file_path, 'w') as file:
        file.write("import pygame\n")
        file.write("import math\n")
        file.write("import random\n")
        file.write("import time\n")

        for class_def in class_definitions:
            file.write(class_def + "\n\n")

    

    print("games.py file updated successfully with the latest classes")

    
def get_images():
    shutil.rmtree("assets")
    assets_folder = "assets"
    if not os.path.exists(assets_folder):
        os.makedirs(assets_folder)
    try:
        # Send a GET request to the Flask server to fetch images
        response = requests.get(f"http://{server_ip}:5000/get_images")  # Update the URL if your Flask app runs elsewhere
        response.raise_for_status()  # Raise an error for bad responses
        images = response.json().get("image_files", {})
        
        print("Images found:")
        
        # Iterate over the image files
        for filename, encoded_image in images.items():
            # Decode the base64 string to binary
            image_data = base64.b64decode(encoded_image)
            
            # Create the full path for the image file
            image_path = os.path.join(assets_folder, filename)
            
            # Save the image data to a file
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data)
                
            print(f"Downloaded and saved: {filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching images: {e}")











    
        
def get_image_from_server():
    try:
        SERVER_URL  = 'http://localhost:5000/get_random_ad_image'
        # Send a GET request to the server
        response = requests.get(SERVER_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()
        if "error" in data:
            print(f"Error: {data['error']}")
            return None

        # Decode the base64 image
        image_data = base64.b64decode(data["image"])
        image = Image.open(BytesIO(image_data))
        image = ImageTk.PhotoImage(image)
        return image

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
