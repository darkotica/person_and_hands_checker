import requests
import pytest


person_with_2_hands_above_head = [
    "test_images/photo_1_person_2_hands_above_head_1.jpg",
    "test_images/photo_1_person_2_hands_above_head_2.png",
    "test_images/photo_1_person_2_hands_above_head_3.jpg",
    "test_images/photo_1_person_2_hands_above_head_4.jpg",
    "test_images/photo_1_person_2_hands_above_head_5.png",
    "test_images/photo_1_person_2_hands_above_head_6.png",
    "test_images/photo_1_person_2_hands_above_head_7.png",
    "test_images/photo_1_person_2_hands_above_head_8.png"
]

person_with_2_hands_bellow_head = [
    "test_images/photo_1_person_2_hands_bellow_head_1.jpg",
    "test_images/photo_1_person_2_hands_bellow_head_2.png",
    "test_images/photo_1_person_2_hands_bellow_head_3.png",
    "test_images/photo_1_person_2_hands_bellow_head_4.png",
    "test_images/photo_1_person_2_hands_bellow_head_5.png",
    "test_images/photo_1_person_2_hands_bellow_head_6.png"
]


def test_send_request_without_file_and_check_response():
    response = requests.post("http://localhost:5000/head-hand-detection")
    assert response.status_code == 400
    assert response.content.decode("utf-8") == "Image not sent in request"


def test_send_request_with_image_but_wrong_param_name_and_check_response():
    test_image = open("test_images/photo_1_person_2_hands_bellow_head_1.jpg",
                      'rb')
    image_param = {'some_image': test_image}
    response = requests.post("http://localhost:5000/head-hand-detection",
                             files=image_param)
    test_image.close()

    assert response.status_code == 400
    assert response.content.decode("utf-8") == "Image not sent in request"


def test_send_request_with_wrong_file_type_and_check_response():
    test_image = open("test_images/photo_wrong_format.avif", 'rb')
    image_param = {'image': test_image}
    response = requests.post("http://localhost:5000/head-hand-detection",
                             files=image_param)
    test_image.close()

    assert response.status_code == 400
    assert response.content.decode("utf-8") == "File must be an image in " \
                                               ".png, .jpg or .jpeg format!"


def test_send_request_with_image_and_check_response():
    test_image = open("test_images/photo_1_person_2_hands_bellow_head_1.jpg",
                      'rb')
    image_param = {'image': test_image}
    response = requests.post("http://localhost:5000/head-hand-detection",
                             files=image_param)
    test_image.close()

    assert response.status_code == 200


def test_send_image_without_people_and_check_response():
    test_image = open("test_images/photo_no_people_1.png", 'rb')
    image_param = {'image': test_image}
    response = requests.post("http://localhost:5000/head-hand-detection",
                             files=image_param)
    test_image.close()

    assert response.status_code == 200
    assert response.content.decode("utf-8") == "There are no " \
                                               "people in the photo!"


def test_send_image_with_more_than_one_person_and_check_response():
    test_image = open("test_images/photo_multiple_people.png", 'rb')
    image_param = {'image': test_image}
    response = requests.post("http://localhost:5000/head-hand-detection",
                             files=image_param)
    test_image.close()

    assert response.status_code == 200
    assert response.content.decode("utf-8") == "There is more than one " \
                                               "person in the photo!"


def test_send_image_with_person_one_or_no_hands_shown_and_check_response():
    test_image = open("test_images/photo_1_person_1_hand.png", 'rb')
    image_param = {'image': test_image}
    response = requests.post("http://localhost:5000/head-hand-detection",
                             files=image_param)
    test_image.close()

    assert response.status_code == 200
    assert response.content.decode("utf-8") == "There are less than 2 " \
                                               "hands in the photo!"


@pytest.mark.parametrize("image_path", person_with_2_hands_bellow_head)
def test_send_image_with_person_hands_bellow_head(image_path):
    test_image = open(image_path, 'rb')
    image_param = {'image': test_image}
    response = requests.post("http://localhost:5000/head-hand-detection",
                             files=image_param)
    test_image.close()

    assert response.status_code == 200
    assert response.content.decode("utf-8") == "This person does not have" \
                                               " both hand raised " \
                                               "above their head!"


@pytest.mark.parametrize("image_path", person_with_2_hands_above_head)
def test_send_image_with_person_hands_above_head(image_path):
    test_image = open(image_path, 'rb')
    image_param = {'image': test_image}
    response = requests.post("http://localhost:5000/head-hand-detection",
                             files=image_param)
    test_image.close()

    assert response.status_code == 200
    assert response.content.decode("utf-8") == "This person has both hands " \
                                               "raised above their head!"




