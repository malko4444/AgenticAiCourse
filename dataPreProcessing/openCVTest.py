import cv2

# Load the pre-trained Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start video capture (0 is the default camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw green rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Show the frame
    cv2.imshow('Face Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# import cv2

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# image = cv2.imread("face1.jpeg")
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Detect faces
# faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# # Draw rectangles around faces
# for (x, y, w, h) in faces:
#     cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)

# cv2.imshow("Face Detection", image)
# if cv2.waitKey(0) == 27:
#     cv2.destroyAllWindows()
# # # Open webcam
# # cap = cv2.VideoCapture(0)

# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         break
# #     afterEdgeDetect=cv2.Canny(frame, 100, 200)
#       gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#       faces = face_cascade.detectMultiScale(gray, 1.1, 4)
# #     cv2.imshow("Webcam Feed", afterEdgeDetect)
    
# #     # Press 'q' to exit
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # cap.release()
# # cv2.destroyAllWindows()