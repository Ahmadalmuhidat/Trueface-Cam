import os
import sys
import customtkinter
import cv2
import face_recognition
import threading
import pickle
import time

from queue import Queue
from CameraManager import CameraManager
from DatabaseManager import DatabaseManager
from CTkMessagebox import CTkMessagebox
from QRReader import QRReader

class FaceRecognitionModal(CameraManager, QRReader):
	def __init__(self) -> None:
		try:
			super().__init__()

			self.n_frames = 5
			self.FrameCounter = 0
			self.FramesQueue = Queue()

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def CaptureAndAnalyze(self):
		try:
			cap = cv2.VideoCapture(0)

			while CameraManager.ActivateCapturing:
				ret, frame = cap.read()

				if ret:
					img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
					self.FramesQueue.put(img_rgb)

					FR_thread = threading.Thread(target=self.AnalyzeFace, args=(frame,))
					FR_thread.start()

					QR_thread = threading.Thread(target=self.ReadQRCode, args=(frame,))
					QR_thread.start()

				time.sleep(0.1)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass
  
	def StartCapturing(self):
		try:
			if not DatabaseManager.CurrentClass:
					title = "Error"
					message = "Please select a lecture from the settings"
					icon = "cancel"
					CTkMessagebox(title=title, message=message, icon=icon)
					return

			if not CameraManager.ActivateCapturing:
				if self.CameraActive:
					CameraManager.ActivateCapturing = True

					StopEvent = threading.Event()
					CaptureThread = threading.Thread(target=self.CaptureAndAnalyze)

					CameraManager.CaptureThreads.append(CaptureThread)
					CameraManager.CaptureEvents.append(StopEvent)

					CaptureThread.start()
				else:
					title = "Error"
					message = "Failed to find active cameras"
					icon = "cancel"
					CTkMessagebox(title=title, message=message, icon=icon)
			else:
				title = "Action Failed"
				message = "Camera is already capturing"
				icon = "cancel"
				CTkMessagebox(title=title, message=message, icon=icon)       

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def StopCapturing(self):
		try:
			if CameraManager.ActivateCapturing:
				self.CloseLoadingScreen()
				
				CameraManager.ActivateCapturing = False
				CameraManager.CaptureEvents[0].set()
				CameraManager.CaptureThreads[0].join(timeout=5)
				CameraManager.CaptureThreads.clear()
				CameraManager.CaptureEvents.clear()

			else:
				title = "Action Failed"
				message = "Camera is not capturing"
				icon = "cancel"
				CTkMessagebox(title=title, message=message, icon=icon)    

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def GetTheFace(self, frame):
		try:
			return face_recognition.face_locations(frame)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def CompareFaces(self, TargetID, TargetName, TargetFaceEncode, small_frame, face, index):
		try:
			cam_face_encodings = face_recognition.face_encodings(small_frame, face)
			stored_face_encoding = pickle.loads(TargetFaceEncode)

			results = face_recognition.compare_faces(
				stored_face_encoding,
				cam_face_encodings
			)

			if results[0]:
				self.InsertAttendance(TargetID)
				DatabaseManager.Students.pop(index)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass
	
	def FindFace(self, face, small_frame):
		try:
			for index in range(len(DatabaseManager.Students)):
				target = DatabaseManager.Students[index]
				TargetID = target[0]
				TargetName = target[1]
				TargetFaceEncode = target[5]
				args = (
					TargetID,
					TargetName,
					TargetFaceEncode,
					small_frame,
					face,
					index
				)

				threading.Thread(target=self.CompareFaces, args=args).start()

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
				face = self.GetTheFace(small_frame)

				if (face):
					self.CreateLoadingScreen()

					# args = (face, small_frame)
					# threading.Thread(target=self.findFace, args=args).start()

					for index in range(len(DatabaseManager.Students)):
						target = DatabaseManager.Students[index]
						TargetID = target[0]
						TargetName = target[1]
						TargetFaceEncode = target[5]
						args = (
              TargetID,
              TargetName,
              TargetFaceEncode,
              small_frame,
              face,
              index
						)

						threading.Thread(target=self.CompareFaces, args=args).start()
				else:
					self.CloseLoadingScreen()

			self.FrameCounter += 1

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass

	def CreateLoadingScreen(self):
		try:
			if not self.ScanningLoadingScreenRunning and not self.LoadingScreen:
				self.ScanningLoadingScreenRunning = True

				self.LoadingScreen = customtkinter.CTkToplevel()
				self.LoadingScreen.geometry("300x200")

				self.LoadingScreen.resizable(width=0, height=0)

				self.LoadingScreen.title("")

				if self.LoadingScreen:
					label = customtkinter.CTkLabel(
						self.LoadingScreen,
						text="scanning....",
						font=customtkinter.CTkFont(size=15)
					)
					label.pack(pady=60)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(exc_obj)
			pass