import os
import sys
import customtkinter
import cv2
import face_recognition
import threading
import pickle
import base64

from queue import Queue
from app.core.camera_module import CameraManagerModule
from app.core.data_manager import DataManager
from app.core.qr_reader_module import QR_ReaderModule
from app.controllers.attendance import insert_attendance

class FaceRecognitionModule(QR_ReaderModule):
	def __init__(self) -> None:
		try:
			super().__init__()

			self.n_frames = 5
			self.FrameCounter = 0
			self.FramesQueue = Queue()
			self.camera_manager = CameraManagerModule()

		except Exception as e:
			ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
			fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
			print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
			print(ExceptionObject)
			pass

	def extract_face(self, frame):
		try:
			return face_recognition.face_locations(frame)

		except Exception as e:
			ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
			fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
			print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
			print(ExceptionObject)
			pass

	def compare_face(self, target_id, target_name, target_face_encode, small_frame, face, index):
		try:
			cam_face_encodings = face_recognition.face_encodings(small_frame, face)
			stored_face_encoding = pickle.loads(base64.b64decode(target_face_encode))

			results = face_recognition.compare_faces(
				stored_face_encoding,
				cam_face_encodings
			)

			if results[0]:
				insert_attendance(target_id, target_name)
				DataManager.Students.pop(index)

		except Exception as e:
			ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
			fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
			print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
			print(ExceptionObject)
			pass
	
	def detect_face(self, face, small_frame):
		try:
			for index in range(len(DataManager.Students)):
				student = DataManager.Students[index]
				args = (
					student.id,
					student.first_name,
					student.face_encode,
					small_frame,
					face,
					index
				)

				threading.Thread(
					target=self.compare_face,
					args=args
				).start()

		except Exception as e:
			ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
			fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
			print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
			print(ExceptionObject)
			pass
	
	def analyze_face(self, frame) -> bool:
		try:
			if self.FrameCounter % self.n_frames == 0:
				small_frame = cv2.resize(
					frame,
					(0, 0),
					fx = 0.25,
					fy = 0.25
				)
				face = self.extract_face(small_frame)

				if (face):
					self.create_loaing_screen()

					# args = (face, small_frame)
					# threading.Thread(target=self.findFace, args=args).start()

					for index in range(len(DataManager.Students)):
						student = DataManager.Students[index]
						args = (
              student.id,
              student.first_name,
              student.face_encode,
              small_frame,
              face,
              index
						)

						threading.Thread(
							target = self.compare_face,
							args = args
						).start()
				else:
					self.camera_manager.close_loading_stream()

			self.FrameCounter += 1

		except Exception as e:
			ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
			fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
			print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
			print(ExceptionObject)
			pass

	def create_loaing_screen(self):
		try:
			if not self.ScanningLoadingScreenRunning and not self.LoadingScreen:
				self.ScanningLoadingScreenRunning = True

				self.LoadingScreen = customtkinter.CTkToplevel()
				self.LoadingScreen.geometry("300x200")

				self.LoadingScreen.resizable(
					width = 0,
					height = 0
				)

				self.LoadingScreen.title("")

				if self.LoadingScreen:
					label = customtkinter.CTkLabel(
						self.LoadingScreen,
						text="scanning....",
						font=customtkinter.CTkFont(size = 15)
					)
					label.pack(pady = 60)

		except Exception as e:
			ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
			fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
			print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
			print(ExceptionObject)
			pass