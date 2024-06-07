from flask import Flask, render_template, request
from PIL import Image
import base64
from io import BytesIO
import weaviate
import os
import logging

WEAVIATE_URL = os.getenv('WEAVIATE_URL')
if not WEAVIATE_URL:
    WEAVIATE_URL = 'http://localhost:8080'

# creating the application and connecting it to the Weaviate local host 
app = Flask(__name__) 
app.config["UPLOAD_FOLDER"] = "/temp_images"
client = weaviate.Client(WEAVIATE_URL)

def weaviate_img_search(img_str):
    """
    This function uses the nearImage operator in Weaviate. 
    """
    sourceImage = { "image": img_str}
    print("sending: ", img_str, " for near_img_search")

    weaviate_results = client.query.get(
        "Bottle", ["filepath","brand"]
        ).with_near_image(
            sourceImage, encode=False
        ).with_limit(2).do()
    print("weaviate results is:")
    print(weaviate_results)

    return weaviate_results["data"]["Get"]["Bottle"]


def list_images():
    """
    Checks the static/img folder and returns a list of image paths
    """
    if os.path.exists('./flask-app'):
        img_path = "./flask-app/static/img-bev/"
    elif os.path.exists('./static'):
        img_path = "./static/img-bev/"
    else:
        return []

    images = []
    for file_path in os.listdir(img_path):
        images.append({
            "path": file_path
        })

    return images


if client.is_ready():    
    # Defining the pages that will be on the website 
    @app.route("/") 
    def home(): # home page
        return render_template("index.html", content = list_images())

    @app.route("/process_image", methods = ["POST"]) # save the uploaded image and convert it to base64

    # process the image upload request by converting it to base64 and querying Weaviate
    def process_image():
            uploaded_file = Image.open(request.files['filepath'].stream)
            uploaded_file = uploaded_file.convert('RGB')
            buffer = BytesIO()             
            uploaded_file.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode()

            weaviate_results = weaviate_img_search(img_str)
            print(weaviate_results)

            results = []
            for result in weaviate_results:
                results.append({
                    "path": result["filepath"], 
                    "brand": result["brand"]
                })

            print(f"\n {results} \n")
            return render_template("index.html", content = results, dog_image = img_str)

else:
    print("There is no Weaviate Cluster Connected.")

# run the app
if __name__ == "__main__": 
    app.run(host='0.0.0.0', port='5000')
