from hands_detection import get_hands_bounds_pixels
from face_detection import get_head_upper_bound


def check_head_and_hands(image_path):
    upper_head_bound, num_of_faces = get_head_upper_bound(image_path)
    if num_of_faces == 0:
        return "There are no people in the photo!"
    elif num_of_faces > 1:
        return "There is more than one person in the photo!"

    lower_hands_bounds = get_hands_bounds_pixels(image_path)

    if len(lower_hands_bounds) < 2:
        return "There are less than 2 hands in the photo!"
    elif len(lower_hands_bounds) > 2:
        return "There are more than 2 hands in the photo!"

    num_of_hands_above_head = 0

    for hand in lower_hands_bounds:
        hand_size = hand[1] - hand[0]
        if hand[1] - upper_head_bound <= 0.1*hand_size:
            num_of_hands_above_head += 1

    if num_of_hands_above_head <= 1:
        return "This person does not have both hand raised above their head!"
    else:
        return "This person has both hands raised above their head!"
