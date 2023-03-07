import cv2
import mediapipe as mp


def draw_face_detections(image_path, output_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_face_detection = mp.solutions.face_detection

    image = cv2.imread(image_path)

    for detection in get_face_detections(image_path):
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


def get_head_upper_bound(image_path):
    detections = get_face_detections(image_path)
    num_of_detections = 0 if not detections else len(detections)

    if num_of_detections == 0 or num_of_detections > 1:
        return 0, num_of_detections

    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    bbox = detections[0].location_data.relative_bounding_box
    upper_bound_y = bbox.ymin * image_height

    return upper_bound_y, len(detections)
