import customtkinter
import cv2
import face_recognition
import threading
import pickle
import sys
import os

from queue import Queue
from CameraManager import CameraManager

class FaceRecognitionModal(CameraManager):
	def __init__(self) -> None:
		try:
			super().__init__()

			self.ShowedIDs = []

			self.n_frames = 5
			self.FrameCounter = 0
			self.FramesQueue = Queue()

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def getTheFace(self, frame):
		try:
			return face_recognition.face_locations(frame)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def compareFaces(self, TargetID, TargetName, TargetFaceEncode, small_frame, face, index):
		try:
			cam_face_encodings = face_recognition.face_encodings(small_frame, face)
			stored_face_encoding = pickle.loads(TargetFaceEncode)

			results = face_recognition.compare_faces(stored_face_encoding, cam_face_encodings)

			if results[0]:
				self.ShowedIDs.append(TargetID)
				self.insertAttendance(TargetID)
				self.Students.pop(index)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def checkTargetInShowedIDs(self, targetID):
		try:
			return targetID not in self.ShowedIDs

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def AnalyzeFace(self, frame) -> bool:
		try:
			if self.FrameCounter % self.n_frames == 0:
				small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
				face = self.getTheFace(small_frame)

				if (face):
					self.createLoadingScreen("scanning....")

					for index in range(len(self.Students)):
						target = self.Students[index]
						TargetID = target[0]
						TargetName = target[1]
						TargetFaceEncode = target[3]
						args = (
              TargetID,
              TargetName,
              TargetFaceEncode,
              small_frame,
              face,
              index)

						if self.checkTargetInShowedIDs(TargetID):
							threading.Thread(target=self.compareFaces, args=args).start()
				else:
					self.closeLoadingScreen()

			self.FrameCounter += 1

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def createLoadingScreen(self, message):
		try:
			if not self.ScanningLoadingScreenRunning and not self.LoadingScreen:
				self.ScanningLoadingScreenRunning = True

				self.LoadingScreen = customtkinter.CTkToplevel()
				self.LoadingScreen.geometry("500x200")
				self.LoadingScreen.title("")
				self.LoadingScreen.resizable(width=0, height=0)

				if self.LoadingScreen:
					label = customtkinter.CTkLabel(self.LoadingScreen, text=message, font=customtkinter.CTkFont(size=15))
					label.pack(pady=60)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass