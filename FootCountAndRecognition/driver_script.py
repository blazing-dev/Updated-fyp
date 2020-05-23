from FootCountAndRecognition.encode_faces import Extract_encodings
from FootCountAndRecognition.recognize_faces_video import Recognize_from_LiveStream
from FootCountAndRecognition.people_counter import PeopleCounter
import face_recognition
from imutils.video import VideoStream
from imutils.video import FileVideoStream
import cv2
import time
import imutils
import requests
import numpy as np
from imutils.video import FPS

class DriverForCamera1:
    def __init__(self):
        self.totalFrames = 0
        #self.skippedFrames = 10
        self.vs = VideoStream(src=0).start()
        time.sleep(2.0)
        print("[INFO] starting video stream...")
        self.fps = FPS().start()
        self.recognizerEntry = Recognize_from_LiveStream()
        self.peopleCounterEntry = PeopleCounter()
        self.EncodingExtractor = Extract_encodings()

    def StartEntryCountAndRecognition(self):
        while True:
            # Entry Footage
            frameEntry = self.vs.read()
            frameEntry = imutils.resize(frameEntry, width = 450)
            rgb = cv2.cvtColor(frameEntry, cv2.COLOR_BGR2RGB)
            # r = frame.shape[1]/float(rgb.shape[1])
            boxes = face_recognition.face_locations(rgb, model="cnn")
            entry_line_crossed, entryCount, frameEntry1 = self.peopleCounterEntry.HeadCount(frameEntry, rgb, boxes, self.totalFrames)
            namesOfPeopleEntered, frameEntry2 = self.recognizerEntry.Recognition(frameEntry, rgb, boxes)
            # frameEntry2 = frameEntry1
            # if entry_line_crossed:
            #     # Capture Arrival Time
            #     print("Capture Arrival Time")
            #     print("Names of People Entered", namesOfPeopleEntered)
            #     print("Entry Count", entryCount)

            # cv2.imshow("Entry Frame", cv2.add(frameEntry1, frameEntry2))
            frameEntry3 =  cv2.add(frameEntry1, frameEntry2)
            yield entry_line_crossed, entryCount, namesOfPeopleEntered, frameEntry3
            self.totalFrames += 1
            #     key = cv2.waitKey(1) & 0xFF
            #     if key == ord("q"):
            #         break

        #     self.fps.update()
        # self.fps.stop()
        #
        # print("Total Entry Frames", self.totalFrames)
        # print("[INFO] elapsed time: {:.2f}".format(self.fps.elapsed()))
        # print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))

        # cv2.destroyAllWindows()
        # self.vs.stop()

class DriverForCamera2():
    def __init__(self):
         self.url = "http://192.168.137.31:8080//shot.jpg"
         print("[INFO] starting video stream...")
         self.fps = FPS().start()
         self.totalFrames1 = 0
         self.recognizerExit = Recognize_from_LiveStream()
         self.peopleCounterExit = PeopleCounter()
         self.EncodingExtractor = Extract_encodings()

    def StartExitCountAndRecognition(self):
            while True:
                # Exit Footage
                img_resp = requests.get(self.url)
                img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                frameExit = cv2.imdecode(img_arr, -1)
                frameExit = imutils.resize(frameExit, width = 450)
                rgb1 = cv2.cvtColor(frameExit, cv2.COLOR_BGR2RGB)
                boxes1 = face_recognition.face_locations(rgb1, model="cnn")
                exit_line_crossed, exitCount, frameExit1 = self.peopleCounterExit.HeadCount(frameExit, rgb1, boxes1, self.totalFrames1)
                namesOfPeopleLeaving, frameExit2 = self.recognizerExit.Recognition(frameExit, rgb1, boxes1)
                # if exit_line_crossed:
                #     # Capture Departure Time
                #     # Printing for testing
                #     print("Capture Departure Time")
                #     print("Names of People Entered", namesOfPeopleLeaving)
                #     print("Entry Count", exitCount)
                # cv2.imshow("Exit Frame", cv2.add(frameExit1, frameExit2))
            #image = np.array(frame)

            # cv2.imshow("Frame2", frame2)
                frameExit3 = cv2.add(frameExit1, frameExit2)
                yield (exit_line_crossed, exitCount, namesOfPeopleLeaving, frameExit3)
                self.totalFrames1 += 1
            #     self.fps.update()
            #     self.fps.stop()
            #
            # print("Total Exit Frames", self.totalFrames1)
            # print("[INFO] elapsed time: {:.2f}".format(self.fps.elapsed()))
            # print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))


