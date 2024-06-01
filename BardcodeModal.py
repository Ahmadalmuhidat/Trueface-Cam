# import os
# import sys
# import cv2
# # from pyzbar import pyzbar

# class BardcodeModal():
# 	def __init__(self) -> None:
# 		try:
# 			super().__init__()

# 		except Exception as e:
# 			exc_type, exc_obj, exc_tb = sys.exc_info()
# 			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
# 			print(exc_type, fname, exc_tb.tb_lineno)
# 			print(exc_obj)
# 			pass

# 	def decode_barcode(image):
# 		try:
# 			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 			barcodes = pyzbar.decode(gray)

# 			for barcode in barcodes:
# 				(x, y, w, h) = barcode.rect

# 				cv2.rectangle(
# 					image,
# 					(x, y),
# 					(x + w, y + h),
# 					(0, 255, 0),
# 					2
# 				)

# 				barcode_data = barcode.data.decode("utf-8")
# 				barcode_type = barcode.type

# 				text = f"{barcode_data} ({barcode_type})"
# 				# cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 				print(f"Detected barcode: {barcode_data} (Type: {barcode_type})")

# 		except Exception as e:
# 			exc_type, exc_obj, exc_tb = sys.exc_info()
# 			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
# 			print(exc_type, fname, exc_tb.tb_lineno)
# 			print(exc_obj)
# 			pass