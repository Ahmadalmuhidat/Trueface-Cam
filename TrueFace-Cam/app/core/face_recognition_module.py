import os
import sys
import customtkinter
import cv2
import face_recognition
import threading
import pickle
import base64
import time

from threading import Lock
from app.config.context import Context
from app.controllers.attendance import insert_attendance
from concurrent.futures import ThreadPoolExecutor

class Face_Recognition_Module():
	def __init__(self) -> None:
		# private
		self._data_manager = Context()
		self._scan_lock = Lock()
		self._executor = ThreadPoolExecutor(max_workers=5)
		self._last_frame_time = 0
		self._frame_interval = 0.5

	def extract_face(self, frame):
		return face_recognition.face_locations(frame)

	def compare_face(self, target_id, target_name, target_face_encode, small_frame, face_locations, index):
		try:
			if not cam_face_encodings:
				return

			cam_face_encodings = face_recognition.face_encodings(small_frame, face_locations)
			face_distances = face_recognition.face_distance(target_face_encode, cam_face_encodings[0])

			if face_distances < 0.5:
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
				self._executor.submit(self.compare_face, *args)

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
		for student in self._students_to_scan:
			try:
				decoded = pickle.loads(base64.b64decode(student.get_face_encode()))
				student._face_encode = decoded
			except Exception as e:
				print(f"Error decoding face for {student.get_student_id()}: {e}")
	
	def analyze_camera_stream(self, frame) -> bool:
		try:
			current_time = time.time()
			if current_time - self._last_frame_time >= self._frame_interval:
				self._last_frame_time = current_time
				small_frame = cv2.resize(
					frame,
					(0, 0),
					fx=0.25,
					fy=0.25
				)
				face = self.extract_face(small_frame)

				if face and len(self._students_to_scan) != 0:
					self.detect_face(face, small_frame)
				else:
					self.camera_manager.close_loading_stream()

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