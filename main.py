import cv2
KNOWN_DISTANCE = 76.2  # centimeter
KNOWN_WIDTH = 14.3  # centimeter
# KNOWN_DISTANCE = 340.2  # centimeter
# KNOWN_WIDTH = 155.3  # centimeter
# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
cap = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def reference(measured_distance, real_width, width_in_rf_image):
    reference_length_value = (width_in_rf_image * measured_distance) / real_width
    return reference_length_value
def distance_finder(focal_length, real_face_width, face_width_in_frame):
    distance = (real_face_width * focal_length) / face_width_in_frame
    return distance

def face_data(image):
    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
        face_width = w


    return face_width

ref_image = cv2.imread("frame-3.png")

ref_image_face_width = face_data(ref_image)
focal_length_found = reference(KNOWN_DISTANCE, KNOWN_WIDTH, ref_image_face_width)
print(focal_length_found)
cv2.imshow("ref_image", ref_image)
cv2.waitKey(0)
while True:
    _, frame = cap.read()
    cv2.waitKey(0)
    face_width_in_frame = face_data(frame)
    if face_width_in_frame != 0:
        Distance = distance_finder(focal_length_found, KNOWN_WIDTH, face_width_in_frame)
        cv2.putText(
            frame, f"Distance = {round(Distance, 2)} CM", (50, 50), fonts, 1, (WHITE), 2
        )
    cv2.imshow("frame", frame)