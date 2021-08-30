import cv2
from pyo import *
import multiprocessing
import HandTrackingModule as hts
import Synth
import GUI

if __name__ == '__main__':
    synth_queue = multiprocessing.Queue()
    control_queue = multiprocessing.Queue()
    synth_control_queue = multiprocessing.Queue()

    gui = GUI.GUIProc(control_queue)
    gui.start()
    synth = Synth.SynthProc(synth_queue, synth_control_queue, 60)
    synth.start()
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = hts.HandDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, fingerNumbers=[5, 8, 9, 12, 13, 16, 17, 20])
        if len(lmList) == 8:
            rootX = lmList[1][0]
            if (lmList[0][1] - lmList[1][1]) > 50:
                rootY = lmList[1][1]
            else:
                rootY = 0

            if (lmList[3][0] - lmList[1][0]) > 60:
                thirdQuality = 1
            else:
                thirdQuality = 0

            if (lmList[2][1] - lmList[3][1]) > 50:
                thirdY = rootY
            else:
                thirdY = 0

            if (lmList[5][0] - lmList[3][0]) > 60:
                fifthQuality = 1
            else:
                fifthQuality = 0
            if (lmList[4][1] - lmList[5][1]) > 50:
                fifthY = rootY
            else:
                fifthY = 0

            if (lmList[7][0] - lmList[5][0]) > 60:
                seventhQuality = 1
            else:
                seventhQuality = 0
            if (lmList[6][1] - lmList[7][1]) > 50:
                seventhY = rootY
            else:
                seventhY = 0

            synth_queue.put([rootX, rootY, thirdQuality, thirdY, fifthQuality, fifthY, seventhQuality, seventhY])
        else:
            synth_queue.put((0, 0, 0, 0, 0, 0, 0, 0))

        if not control_queue.empty():
            control_data = control_queue.get()
            if control_data == -1:
                synth.terminate()
                break
            else:
                synth_control_queue.put(control_data)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

