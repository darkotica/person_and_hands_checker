import os.path

from flask import Flask, request, make_response
from werkzeug.utils import secure_filename
from head_and_hands_checker import check_head_and_hands


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['TEST_IMAGES'] = 'test_images'


@app.route('/head-hand-detection', methods=['POST'])
def head_and_hand_detection():
    if 'image' not in request.files or not request.files["image"]:
        return make_response("Image not sent in request", 400)

    sent_image = request.files['image']

    if not sent_image.filename.endswith(('.png', '.jpg', 'jpeg')):
        return make_response("File must be an image in .png, .jpg or"
                             " .jpeg format!", 400)

    filename = secure_filename(sent_image.filename)
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    image_filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    sent_image.save(image_filepath)

    try:
        results = check_head_and_hands(image_filepath)
        os.remove(image_filepath)
        return make_response(results, 200)
    except Exception as e:
        print(e)
        os.remove(image_filepath)
        return make_response("Internal server error.\n" + str(e), 500)


if __name__ == '__main__':
    app.run()
