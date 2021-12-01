import cv2
import numpy as np
import time
import PoseModule as pm
import os
import AudioCommSys as audio_sys

class utilities():
    def __init__(self) -> None:
        pass

    def repitition_counter(self, per, count, direction):
        if (per == 100 and direction == 0):
            count += 0.5
            direction = 1
        if (per == 0 and direction == 1):
            count += 0.5
            direction = 0
            if int(count) != 0:
                audio_sys.text_to_speech(str(int(count)))
        return {"count": count, "direction":  direction}

    def draw_performance_bar(self, img, per, bar, color, count):
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

    def show_workout_example(self, example, exercise):
        seconds = 5
        while seconds >= 0:
            img = cv2.imread(example)
            img = cv2.resize(img, (1280, 720))
            cv2.putText(img, exercise + " in: " + str(int(seconds)) , (500, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 10)    
            cv2.imshow("Image", img)  
            time.sleep(1)
            seconds -= 1
            cv2.waitKey(1)

    def get_bar_color(self, per):
        color =  (0, 205, 205)
        if 0 < per <= 30:
            color = (51, 51, 255)
        if 30 < per <= 60:
            color = (0, 165, 255)
        if 60 <= per <= 100:
            color = (0, 255, 255)
        return color

class simulate_upper_body_trainer():
    def __init__(self, difficulty_level = 1, reps=2, calories_burned = 0):
        self.reps = reps
        self.difficulty_level = difficulty_level
        self.calories_burned = calories_burned

    def bicep_curls(self):
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while True:
            img = cv2.imread('TrainerData/Thumb3.jpg')
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)

            if len(landmark_list) != 0:
                left_arm_angles = detector.find_angle(img, 13, 11, 12)
                left_arm_angle1 = detector.find_angle(img, 11, 13, 15)
                left_arm_angle = detector.find_angle(img, 12, 14, 16)
                per = np.interp(left_arm_angle, (210, 310), (0, 100))
                bar = np.interp(left_arm_angle, (220, 310), (650, 100))
               
                color = utilities().get_bar_color(per)
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            cv2.putText(img, str(int(count)) + "/"+ str(self.reps * self.difficulty_level), (40, 220), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)  
            cv2.imshow("Image", img)
            cv2.waitKey(1)

            time_elapsed = int(time.process_time() - start)
            self.calories_burned = 20
    
class start_workout_session():
    def __init__(self, difficulty_level=1):
        self.difficulty_level = difficulty_level

    def completion_screen(self, congrats_img):
        seconds = 4
        while seconds >= 0:
            img = cv2.imread(congrats_img)
            img = cv2.resize(img, (1280, 720))
            cv2.imshow("Image", img)  
            time.sleep(1)
            seconds -= 1
            cv2.waitKey(1)

    def complete_path(self):
        simulator_ub = simulate_upper_body_trainer(self.difficulty_level)
        simulator_ub.bicep_curls()

def main():  
    session = start_workout_session()
    performance = session.complete_path()
    print(performance)

if __name__ == "__main__":
    main()
