# pip install mediapipe opencv-python numpy

import cv2
import mediapipe as mp
import numpy as np

# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def drawBoundingBoxes(image, results, padd_amount = 10, draw=True):
    output_image = image.copy()
    height, width, _ = image.shape

    for _, hand_landmarks in enumerate(results.multi_hand_landmarks):
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))

        x_coordinates = np.array(landmarks)[:,0]
        y_coordinates = np.array(landmarks)[:,1]

        x1  = int(np.min(x_coordinates) - padd_amount)
        y1  = int(np.min(y_coordinates) - padd_amount)
        x2  = int(np.max(x_coordinates) + padd_amount)
        y2  = int(np.max(y_coordinates) + padd_amount)

        if draw:
            cv2.rectangle(output_image, (x1, y1), (x2, y2), (155, 0, 255), 3, cv2.LINE_8)
            # cv2.putText(output_image, label, (x1, y2+25), cv2.FONT_HERSHEY_COMPLEX, 0.7, (20,255,155), 1, cv2.LINE_AA)
        coords = ((x1,y1), (x2,y2))
        return output_image, coords

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  fc = 0
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
      image, ((x1,y1), (x2,y2)) = drawBoundingBoxes(image, results, padd_amount=40)
      if fc % 10 == 0:
        img_crop = image[y1:y2, x1:x2]
        try:
          cv2.imwrite(f'./img/{fc}.jpg', img_crop)
        except:
          print("Cannot save empty frame")

    cv2.imshow("asl", image)
    fc += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break


cap.release()
cv2.destroyAllWindows()
