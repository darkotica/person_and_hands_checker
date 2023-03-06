from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/head-hand-detection', methods=['POST'])
def head_and_hand_detection():
    if 'image' not in request.files or not request.files["image"]:
        return make_response("Image not sent in request", 400)

    sent_image = request.files['image']

    return make_response("Image succesfuly sent", 200)


if __name__ == '__main__':
    app.run()
