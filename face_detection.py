from hashlib import sha3_384
import cv2
import enum
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
import time

  
# importing os module  
import os
  

import inspect

# # For static images:
# IMAGE_FILES = []
# with mp_face_detection.FaceDetection(
#     model_selection=1, min_detection_confidence=0.5) as face_detection:
#   for idx, file in enumerate(IMAGE_FILES):
#     image = cv2.imread(file)
#     # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
#     results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # Draw face detections of each face.
#     if not results.detections:
#       continue
#     annotated_image = image.copy()
#     for detection in results.detections:
#       print('Nose tip:')
#       print(mp_face_detection.get_key_point(
#           detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
#       mp_drawing.draw_detection(annotated_image, detection)
#     cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

# For webcam input:
# cap = cv2.VideoCapture(0)
# with mp_face_detection.FaceDetection(
#     min_detection_confidence=0.5) as face_detection:
#   while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue

#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = face_detection.process(image)

#     # Draw the face detection annotations on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     if results.detections:
#       for detection in results.detections:
#         mp_drawing.draw_detection(image, detection)
#     # Flip the image horizontally for a selfie-view display.
#     cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()

class FaceKeyPoint(enum.IntEnum):
  """The enum type of the six face detection key points."""
  RIGHT_EYE = 0
  LEFT_EYE = 1
  NOSE_TIP = 2
  MOUTH_CENTER = 3
  RIGHT_EAR_TRAGION = 4
  LEFT_EAR_TRAGION = 5

def get_direction_of_person():
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(
        min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)

            # Draw the face detection annotations on the image.
            # image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)
                    # get dimensions of image
                    dimensions = image.shape
                    
                    # height, width, number of channels in image
                    height = image.shape[0]
                    width = image.shape[1]
                    
                    print('Image Dimension    : ',dimensions)
                    print('Image Height       : ',height)
                    print('Image Width        : ',width)


                    # Convert the normalized points to actual points on the image according to height and width
                    # print('Nose tip:')
                    # print(mp_face_detection.get_key_point(
                    # detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
                    nose_x_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.NOSE_TIP).x * width
                    nose_y_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.NOSE_TIP).y * height

                    # print('Right ear:')
                    # print(mp_face_detection.get_key_point(
                    # detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION))
                    right_ear_x_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION).x * width
                    right_ear_y_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION).y * height


                    # print('Left ear:')
                    # print(mp_face_detection.get_key_point(
                    # detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION))

                    left_ear_x_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).x * width
                    left_ear_y_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).y * height



                    if left_ear_x_axis < nose_x_axis:
                        print("TOO TO THE LEFT")

                    if right_ear_x_axis > nose_x_axis:
                        print("TOO TO THE RIGHT")

                    # print('Left eye:')
                    # print(mp_face_detection.get_key_point(
                    # detection, mp_face_detection.FaceKeyPoint.LEFT_EYE))

                    left_eye_x_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.LEFT_EYE).x * width
                    left_eye_y_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.LEFT_EYE).y * height


                    # print('Right eye:')
                    # print(mp_face_detection.get_key_point(
                    # detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE))

                    right_ear_x_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE).x * width
                    right_ear_y_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE).y * height


                    # print('Mouth center:')
                    # print(mp_face_detection.get_key_point(
                    # detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER))

                    mouth_center_x_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).x * width
                    mouth_center_y_axis = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).y * height

            else:
                print("NO FACE")
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()


# Position of camera is directyly by the side
def is_in_right_direction(img,  shoulder_x1,shoulder_x2, waist_x1):
    # Cropped Image
    if waist_x1 > shoulder_x1:
        return False
    
    return True

def is_person_facing_front(img, shoulder_x1, shoulder_y1,  shoulder_x2, shoulder_y2):
    # Cropped Image
    if shoulder_x1 > shoulder_x2:
        return False
    
    image = img[0:shoulder_y1, shoulder_x1:shoulder_x2]

    # Image directory
    directory = os.getcwd()

    print("Before saving image:")  
    
    # Filename
    filename = 'savedImage.jpg'
    
    # Using cv2.imwrite() method
    # Saving the image
    cv2.imwrite(filename, image)
    
    # List files and directories  
    # in 'C:/Users / Rajnish / Desktop / GeeksforGeeks'  
    print("After saving image:")  
    print(os.listdir(directory))
    print('Successfully saved')

    
    with mp_face_detection.FaceDetection(
       min_detection_confidence=0.5) as face_detection:
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # If there is no face at all return False
        if not results.detections:
            print("NO DETECTIONS")
            return False

        for detection in results.detections:
            height = image.shape[0]
            width = image.shape[1]                 
            dimensions = image.shape
                    
            print('Image Dimension    : ',dimensions)
            print('Image Height       : ',height)
            print('Image Width        : ',width)

            nose_x_axis = mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.NOSE_TIP).x * width
            nose_y_axis = mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.NOSE_TIP).y * height

            right_ear_x_axis = mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION).x * width
            right_ear_y_axis = mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION).y * height

            left_ear_x_axis = mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).x * width
            left_ear_y_axis = mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).y * height

            left_eye_x_axis = mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.LEFT_EYE).x * width
            left_eye_y_axis = mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.LEFT_EYE).y * height

            right_eye_x_axis = mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE).x * width
            right_eye_y_axis = mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE).y * height

            mouth_center_x_axis = mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).x * width
            mouth_center_y_axis = mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).y * height

            if left_ear_x_axis < nose_x_axis:
                print("TOO TO THE LEFT")
                cv2.imshow("Image", image)
                return False

            if right_ear_x_axis > nose_x_axis:
                print("TOO TO THE RIGHT")
                cv2.imshow("Image", image)
                return False

            else:
                print("FACING FOWARD")
                cv2.imshow("Image", image)
                return True

            

        






