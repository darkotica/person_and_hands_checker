import mediapipe as mp
import cv2


def draw_hand_landmarks(image_path, output_image_path):
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    image = cv2.imread(image_path)
    image = cv2.flip(image, 1)

    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in get_hand_landmarks_from_image(image_path):
        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    cv2.imwrite(output_image_path, cv2.flip(annotated_image, 1))


def get_hand_landmarks_from_image(image_path):
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode=True,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=2)

    image = cv2.imread(image_path)
    image = cv2.flip(image, 1)

    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    return results.multi_hand_landmarks


def get_hands_bounds_pixels(image_path, debug=False):
    mp_hands = mp.solutions.hands
    hands = get_hand_landmarks_from_image(image_path)

    if not hands:
        return []

    image = cv2.imread(image_path)
    image = cv2.flip(image, 1)

    image_height, image_width, _ = image.shape
    hands_bound_pixels = []
    for hand_landmarks in hands:
        landmarks_y = [hand_landmarks.landmark[key].y
                       for key in mp_hands.HandLandmark]
        lower_bound_y = min(landmarks_y) * image_height
        upper_bound_y = max(landmarks_y) * image_height
        hands_bound_pixels.append((lower_bound_y, upper_bound_y))

    return hands_bound_pixels
