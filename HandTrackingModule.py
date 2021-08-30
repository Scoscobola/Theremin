import cv2
import mediapipe as mp


class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionConfidence=0.8, trackConfidence=0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionConfidence, self.trackConfidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, fingerNumbers=None, draw=True):
        lmList = []

        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            #print(list(enumerate(myHand.landmark)))
            if fingerNumbers is None:
                for id, lm in enumerate(myHand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

            else:
                for id, lm in list(enumerate(myHand.landmark)):
                    if id in fingerNumbers:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([cx, cy])

        return lmList
