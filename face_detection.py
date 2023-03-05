import cv2
import mediapipe as mp


def draw_face_detections(image_path, detections, output_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_face_detection = mp.solutions.face_detection

    image = cv2.imread(image_path)

    for detection in detections:
        print('Nose tip:')
        print(mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
        mp_drawing.draw_detection(image, detection)

    cv2.imwrite(output_path, image)


def get_face_detections(image_path):
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5) as face_detection:

        image = cv2.imread(image_path)
        # Convert the BGR image to RGB and process
        # it with MediaPipe Face Detection.
        results = face_detection.process(cv2.cvtColor(image,
                                                      cv2.COLOR_BGR2RGB))

        return results.detections


def get_upper_bound_head(image_path):
    detections = get_face_detections(image_path)

    if len(detections) != 1:
        return None

    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    bbox = detections[0].location_data.relative_bounding_box
    upper_bound_y = (bbox.ymin - 0.1 * bbox.height) * image_height

    # cv2.line(image, (0, int(upper_bound_y)),
    #          (image_width, int(upper_bound_y)), (0, 255, 0),
    #          thickness=2)
    #
    # cv2.imwrite("./test_images/head_line.png", image)
    return upper_bound_y


# get_upper_bound_head("test_images/face_image_1.jpg")
# draw_face_detections("test_images/face_image_1.jpg",
#                      get_face_detections("test_images/face_image_1.jpg"),
#                      "test_images/face_annotated_image_1.png")
