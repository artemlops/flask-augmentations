import io
import requests
import random
from flask import Flask, request, render_template
from PIL import Image
from pathlib import Path

# Imports for prediction
from mymodel.image_augmentations import random_augmentation

CURRENT_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# 4MB Max image size limit
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

# Default route just shows simple text
@app.route('/', methods=['GET'])
def index():
    # TODO: improve UX: say explicitly that 'url' param is required
    image_url = request.args.get('url')
    print(image_url)
    # TODO: white-list domain names for security reasons
    image_response = requests.get(image_url)
    image = Image.open(io.BytesIO(image_response.content))
    flipped_image = random_augmentation(image)
    # TODO: support multi-processing: do not save to the same file
    flipped_image.save(CURRENT_DIR / "static/augmented_image.jpg")
    return render_template("index.html")

if __name__ == '__main__':
    # TODO: expose parameters (port, seed, etc)
    random.seed(42)
    # Run the server
    app.run(host='0.0.0.0', port=8000, debug=True)

