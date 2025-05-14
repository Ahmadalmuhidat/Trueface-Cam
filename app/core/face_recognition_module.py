import os
import sys
import customtkinter
import cv2
import face_recognition
import threading
import pickle
import base64

from queue import Queue
from threading import Lock
from app.core.data_manager import Data_Manager
from app.core.qr_reader_module import QR_Reader_Module
from app.controllers.attendance import insert_attendance


class Face_Recognition_Module():
	def __init__(self) -> None:
		# private
		self._n_frames = 5
		self._frame_counter = 0
		self._frames_queue = Queue()
		self._qr_reader = QR_Reader_Module()
		self._data_manager = Data_Manager()
		self._scan_lock = Lock()

	def extract_face(self, frame):
		return face_recognition.face_locations(frame)

	def compare_face(self, target_id, target_name, target_face_encode, small_frame, face, index):
		try:
			cam_face_encodings = face_recognition.face_encodings(small_frame, face)
			stored_face_encoding = pickle.loads(base64.b64decode(target_face_encode))
			results = face_recognition.compare_faces(
				stored_face_encoding,
				cam_face_encodings
			)

			if results[0]:
				with self._scan_lock:
					threading.Thread(
						target=insert_attendance,
						args=(target_id, target_name)
					).start()
					self._students_to_scan.pop(index)

		except Exception as e:
			ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
			fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
			print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
			print(ExceptionObject)
			pass
	
	def detect_face(self, face, small_frame):
		try:
			for index in range(len(self._students_to_scan)):
				student = self._students_to_scan[index]
				args = (
					student.get_student_id(),
					student.get_first_name(),
					student.get_face_encode(),
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
	
	def start_session(self):
		from app.core.camera_module import Camera_Manager_Module
		self.camera_manager = Camera_Manager_Module()
		self._students_to_scan = self._data_manager.get_current_class_students()
	
	def analyze_camera_stream(self, frame) -> bool:
		try:
			if self._frame_counter % self._n_frames == 0:
				small_frame = cv2.resize(
					frame,
					(0, 0),
					fx = 0.25,
					fy = 0.25
				)
				face = self.extract_face(small_frame)

				if face and len(self._students_to_scan) != 0:
					# self.create_loaing_screen()
					self.detect_face(face, small_frame)
				else:
					self.camera_manager.close_loading_stream()
			self._frame_counter += 1

		except Exception as e:
			ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
			fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
			print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
			print(ExceptionObject)
			pass

	def create_loaing_screen(self):
		try:
			if not self.scanning_loading_screen_running and not self.loading_screen:
				self.scanning_loading_screen_running = True

				self.loading_screen = customtkinter.CTkToplevel()
				self.loading_screen.geometry("300x200")
				self.loading_screen.resizable(
					width = 0,
					height = 0
				)

				self.loading_screen.title("")

				if self.loading_screen:
					label = customtkinter.CTkLabel(
						self.loading_screen,
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