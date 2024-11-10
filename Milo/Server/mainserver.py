from flask import Flask, jsonify, send_from_directory, abort, Response
import os
import json
import base64
import re
import random

app = Flask(__name__)

FILES_FOLDER = "files"

def get_all_files_from_folder(folder_path):
    json_files = []
    image_files = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            if filename.lower().endswith('.json'):
                json_files.append(filename)  # Append only the filename
            elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_files.append(filename)  # Append only the filename

    return json_files, image_files

@app.route("/get_posts", methods=['GET'])
def get_posts():
    json_files, image_files = get_all_files_from_folder(FILES_FOLDER)

    # Create response dict
    response = {
        "json_files": {},
        "image_files": {}
    }

    # Read the JSON files and include their contents in the response
    for json_file in json_files:
        with open(os.path.join(FILES_FOLDER, json_file), 'r') as f:
            response["json_files"][json_file] = json.load(f)  # Store file contents

    # Read image files and include their data in the response as base64 strings
    for image_file in image_files:
        with open(os.path.join(FILES_FOLDER, image_file), 'rb') as img:
            encoded_image = base64.b64encode(img.read()).decode('utf-8')  # Encode image data to base64
            response["image_files"][image_file] = encoded_image  # Store base64 encoded image

    return jsonify(response)


@app.route("/get_games", methods=["GET"])
def get_games():
    file_path = os.path.join(os.getcwd(), "Games/games.py")
    print(file_path)
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()  # Read the entire file content
    except FileNotFoundError:
        return jsonify({"error": "games.py file not found"}), 404

    class_definitions = re.findall(r'class\s+\w+\(.*?\):(?:\n    .*)*', file_content, re.DOTALL)

    return jsonify({"games": class_definitions})

@app.route("/get_images", methods=["GET"])
def get_images():
    assets_path = os.path.join(os.getcwd(), "Games/assets")
    response = {"image_files": {}}

    try:
        # Iterate over all files in the assets folder
        for filename in os.listdir(assets_path):
            file_path = os.path.join(assets_path, filename)
            if os.path.isfile(file_path):
                # Read the image and encode it as base64
                with open(file_path, 'rb') as img_file:
                    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')  # Encode image to base64
                response["image_files"][filename] = encoded_image  # Add the base64 image to the response

        return jsonify(response)
    
    except FileNotFoundError:
        return jsonify({"error": "assets folder not found"}), 404
    











































ADS_FOLDER = "ads"

def get_random_ad_image():
    try:
        # List all image files in the ADS_FOLDER
        image_files = [f for f in os.listdir(ADS_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        if not image_files:
            return None, "No images found in the ads folder."

        # Shuffle the list to select a random file
        random.shuffle(image_files)

        for filename in image_files:
            parts = filename.split("_")
            if len(parts) != 3 or not (parts[0].isdigit() and parts[1].isdigit() and parts[2].split(".")[0].isdigit()):
                continue  # Skip files that don't match the naming convention

            available_id, current_views, max_views = int(parts[0]), int(parts[1]), int(parts[2].split(".")[0])

            if current_views < max_views:
                # Increment the current view count
                new_filename = f"{available_id}_{current_views + 1}_{max_views}.png"
                os.rename(os.path.join(ADS_FOLDER, filename), os.path.join(ADS_FOLDER, new_filename))

                # Read and return the image as base64
                with open(os.path.join(ADS_FOLDER, new_filename), 'rb') as img_file:
                    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
                
                return encoded_image, None

            else:
                # Delete the file if the view count has reached the max
                os.remove(os.path.join(ADS_FOLDER, filename))

        return None, "No valid images found to serve."
    
    except Exception as e:
        return None, str(e)
    
@app.route("/get_random_ad_image", methods=["GET"])
def get_random_ad_image_route():
    encoded_image, error = get_random_ad_image()
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify({"image": encoded_image})















if __name__ == "__main__":
    app.run(debug=True)
