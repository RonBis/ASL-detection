import cv2
from math import floor
import mediapipe as mp

HEIGHT = 720
WIDTH = 720


def resizeAndShow(img: cv2.Mat):
    h, w = img.shape[:2]
    if h < w:
        img = cv2.resize(img, (WIDTH, floor(h/(w/WIDTH))))
    else:
        img = cv2.resize(img, (floor(w/(h/HEIGHT)), HEIGHT))

    cv2.imshow("sign lang", img)
    cv2.waitKey(0)


images = [
    cv2.imread("./img/182781.jpg"),
    cv2.imread("./img/340429.jpg"),
    cv2.imread("./img/5042636.jpg"),
    cv2.imread("./img/645475.jpg"),
    cv2.imread("./img/Cohen-Linus-Torvalds.jpg"),
    cv2.imread("./img/wp1962184-taylor-swift-2017-wallpapers.jpg"),
    cv2.imread("./img/wp1991803-imagine-dragons-wallpapers.png")
]

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# run mediapipe hands
with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.7) as hands:

    for img in images:
        results = hands.process(
            cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 1))

        print("Handedness: ", results.multi_handedness)

        if results.multi_handedness is None:
            continue

        print("Hand landmarks:")
        h, w, _ = img.shape
        annotated_image = cv2.flip(img.copy(), 1)

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        resizeAndShow(cv2.flip(annotated_image, 1))
