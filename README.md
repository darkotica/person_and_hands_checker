# head-hand-detector
This project is a REST service built in Flask, which has an endpoint that accepts an image as input (which has to be sent via POST request), and determines whether:
- there is a person in a photo
- if both of their hands are above their head

and gives a response based on whether the criteria is satisfied or not. Possible responses are:
- "There are no people in the photo!": this is returned in case no people are detected in the photo
- "There is more than one person in the photo!": this is returned in case multiple people are detected in the photo
- "There are less than 2 hands in the photo!": this is returned in case a person is detected, but both hands are not detected in the image (detector found only one or no hands)
- "This person has both hands raised above their head!": this is returned in case a person and both of their hands are detected, and both hands are above their head
- "This person does not have both hand raised above their head!": this is returned in case a person and both of their hands are detected, but not both hands are above their head (only one or no hands are above their head)

## About the service
### Face and head detection
Service uses [Mediapipe](https://google.github.io/mediapipe/) framework for face and hand detection using its [FaceDetection](https://google.github.io/mediapipe/solutions/face_detection.html) and [Hands](https://google.github.io/mediapipe/solutions/hands.html) solution.
<br><br>
In this case, FaceDetection model returns the bounding box of the detected human face, which contains the information about the upper bound of the person's head in the photo. This information will be compared to the lower bounds of found hands.
<br><br>
In case of hands, Hands landmark model returns the keypoints for each detected hand (palm, index finger, thumb etc). Hands' upper and lower bounds are calculated by finding the highest and lowest keypoint of each hand, which represent upper and lower bounds for each hands.
<br><br>
After this, the programme determines whether found hands are above detected face by comparing upper bound of head, and lower bounds of both hands. In addition to this, hands' sizes are also taken in consideration (calulated by deducing lower from upper bounds of hands), in order to provide a 10% error margin (if a hand is at least 90% above the upper bound of the head, it is considered to be above the head).

### Server
This service is implemented using Flask, which is a python web framework. It has one POST endpoint, which is on path /head-hand-detection. This route takes one POST param, which is called 'image', and should be an image file that is sent to the service.

## Running the service
In order to create the docker image of the service, you should enter the following command in the terminal (placed in the project's root folder):
```console
docker build --tag person-hand-detector .
``` 
After building is finished, in order to create docker container running locally (default port is 5000) you should enter the following command:
```console
docker run -d -p 5000:5000 person-hand-detector
``` 
After which the service is accessible on localhost:5000.
<br><br>
To use the service, send a POST request to localhost:5000/head-hand-detection, with image file sent as POST parameter named 'image'.

## Running the tests
In order to run the tests of service's endpoint, pytest and requests libraries should be installed:
```console
pip install pytest
``` 
```console
pip install requests
``` 
After which you should position yourself in command line in 'tests' folder and enter the following command:
```console
pytest
``` 
