import io
import logging
import random
from pathlib import Path

import requests
from flask import Flask, render_template, request
from PIL import Image

from mymodel.image_augmentations import apply_random_augmentations


CURRENT_DIR = Path(__file__).parent

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
# 4MB Max image size limit
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024


@app.route("/", methods=["GET"])
def index():
    context = {}
    # TODO: improve UX: say explicitly that 'url' param is required
    image_url = request.args.get("url")
    logging.debug(f"Image URL: {image_url}")
    # TODO: white-list domain names for security reasons
    image_response = requests.get(image_url)
    # TODO: expose n and other params
    n = random.randint(0, 10)

    image = Image.open(io.BytesIO(image_response.content))
    flipped_image, info = apply_random_augmentations(image, n=n)
    context["transforms"] = info
    logging.debug(f"Applied transforms: {info}")

    # TODO: support multi-processing: do not save to the same file
    flipped_image.save(CURRENT_DIR / "static/augmented_image.jpg")
    return render_template("index.html", **context)


if __name__ == "__main__":
    # TODO: expose parameters (port, seed, etc)
    random.seed(42)
    # Run the server
    app.run(host="0.0.0.0", port=8080, debug=True)
