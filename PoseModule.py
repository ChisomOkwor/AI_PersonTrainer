import mediapipe as mp
import math
import cv2


class posture_detector():
    def __init__(self, mode=False, up_body=False, smooth=True,
                 detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.up_body = up_body
        self.smooth = smooth
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode, self.up_body, self.smooth,
                                      self.detection_con, self.track_con)

    def find_person(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(
                img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return img

    def find_landmarks(self, img, draw=True):
        self.landmark_list = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.landmark_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.landmark_list

    # Given any three points/co-ordinates, it gives us an angle(joint)
    def find_angle(self, img, p1, p2, p3, draw = True):
        # Get the landmarks
        x1, y1 = self.landmark_list[p1][1:]
        x2, y2 = self.landmark_list[p2][1:]
        x3, y3 = self.landmark_list[p3][1:]
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        print("ANGLE")
        print(angle)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 5)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 5)
            cv2.circle(img, (x1, y1), 11, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 16, (255, 60, 0), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 16, (255, 60, 0), 2)
            cv2.circle(img, (x3, y3), 11, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 16, (255, 60, 0), 2)
        
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 60),
            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
        return angle


def main():
    cap = cv2.VideoCapture('TrainerData/facing_back.mp4')
    detector = posture_detector()
    while True:
        success, img = cap.read()
        img = detector.find_person(img)
        landmark_list = detector.find_landmarks(img, draw=True)
        print(landmark_list)
        if len(landmark_list) != 0:
            print(landmark_list[14])
            cv2.circle(
                img, (landmark_list[14][1], landmark_list[14][2]), 15, (0, 0, 255), cv2.FILLED)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break


if __name__ == "__main__":
    main()
