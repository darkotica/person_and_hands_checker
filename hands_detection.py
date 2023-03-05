import mediapipe as mp
import cv2


def get_hand_landmarks_from_image(image_path): # './test_images/face_image_1.jpg'
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode=True,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2)

    image = cv2.imread(image_path)
    image = cv2.flip(image, 1)

    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    return results.multi_hand_landmarks


def draw_hand_landmarks(image_path, hand_landmarks,
                                   output_image_path):
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    image = cv2.imread(image_path)
    image = cv2.flip(image, 1)

    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in hand_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    cv2.imwrite(output_image_path, cv2.flip(annotated_image, 1))


def get_lower_bound_hands(image_path):
    mp_hands = mp.solutions.hands
    hands = get_hand_landmarks_from_image(image_path)

    image = cv2.imread(image_path)
    image = cv2.flip(image, 1)

    image_height, image_width, _ = image.shape
    print(image.shape)
    lower_bound_pixels = []
    for hand_landmarks in hands:
        wrist_pos = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
        print(wrist_pos)
        lower_bound_y = wrist_pos.y * image_height
        lower_bound_pixels.append(lower_bound_y)

        # cv2.line(image, (0, int(lower_bound_y)),
        #          (image_width, int(lower_bound_y)), (0, 255, 0),
        #          thickness=2)

    #cv2.imwrite("./test_images/hand_line.png", cv2.flip(image, 1))

    return lower_bound_pixels


# print(get_lower_bound_hands_pixels("./test_images/hand_image_1.png"))
# draw_hand_landmarks_from_image("./test_images/hand_image_1.png",
#                                get_hand_landmarks_from_image("./test_images/"
#                                                              "hand_image_1."
#                                                              "png"),
#                                "./test_images/hand_annotated_image_0.png")
