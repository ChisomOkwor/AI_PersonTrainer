import cv2
import numpy as np
import time

import PoseModule as pm
import os

from AudioCommSys import text_to_speech
import threading

import face_detection as face_det

from camera import VideoCamera


class utilities:
    list_threads = []

    def __init__(self) -> None:
        pass

    def illustrate_exercise(self, example, exercise):
        seconds = 4
        img = cv2.imread(example)
        img = cv2.resize(img, (980, 550))

        # cv2.imshow("Exercise Illustration", img)
        # cv2.waitKey(1)

        instruction = "Up next is " + exercise + " IN!"

        if exercise != "Warm Up":
            text_to_speech(instruction)

        while seconds > 0:
            img = cv2.imread(example)
            img = cv2.resize(img, (980, 550))
            print("in here1")

            time.sleep(1)
            speaker_thread = threading.Thread(
                target=text_to_speech, args=(str(int(seconds))), kwargs={}
            )
            speaker_thread.start()
            speaker_thread.join()
            cv2.putText(
                img,
                exercise + " in: " + str(int(seconds)),
                (350, 50),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 0, 255),
                5,
            )

            ret, jpeg = cv2.imencode(".jpg", img)

            print("yielding or naaaaaaa")
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            # cv2.imshow("Exercise Illustration", img)
            seconds -= 1
            # cv2.waitKey(1)
        # cv2.destroyAllWindows()

    def repitition_counter(self, per, count, direction):
        list_threads = []
        if per == 100 and direction == 0:
            count += 0.5
            direction = 1
        if per == 0 and direction == 1:
            count += 0.5
            direction = 0
            if int(count) != 0:
                print("here")
                speaker_thread = threading.Thread(
                    target=text_to_speech, args=(str(int(count))), kwargs={}
                )
                list_threads.append(speaker_thread)
                speaker_thread.start()
                # speaker_thread.join()

            # for t in list_threads:
            #     t.join()

        return {"count": count, "direction": direction}

    def display_rep_count(self, img, count, total_reps):
        cv2.rectangle(img, (0, 0), (550, 300), (255, 255, 255), cv2.FILLED)
        cv2.putText(
            img,
            str(int(count)) + "/" + str(total_reps),
            (40, 220),
            cv2.FONT_HERSHEY_PLAIN,
            15,
            (0, 0, 255),
            25,
        )

    def get_performance_bar_color(self, per):
        color = (0, 205, 205)
        if 0 < per <= 30:
            color = (51, 51, 255)
        if 30 < per <= 60:
            color = (0, 165, 255)
        if 60 <= per <= 100:
            color = (0, 255, 255)
        return color

    def position_info_floor_exercise(self, img, isRightPosition):
        if isRightPosition:
            cv2.putText(
                img,
                "Right Position",
                (600, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (0, 0, 255),
                20,
            )
        else:
            cv2.putText(
                img,
                "Incorrect Position",
                (600, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (0, 0, 255),
                20,
            )

    def position_info_standing_exercise(self, img, isRightPosition):
        if isRightPosition:
            cv2.putText(
                img,
                "Facing Foward",
                (600, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (0, 0, 255),
                20,
            )
        else:
            cv2.putText(
                img,
                "Not Facing Foward",
                (600, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (0, 0, 255),
                20,
            )

    def draw_performance_bar(self, img, per, bar, color, count):
        cv2.rectangle(img, (1600, 100), (1675, 650), color, 3)
        cv2.rectangle(img, (1600, int(bar)), (1675, 650), color, cv2.FILLED)
        cv2.putText(
            img, f"{int(per)} %", (1600, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4
        )


class simulate_warmup:
    def __init__(self, difficulty_level=1, reps=2, calories_burned=0):
        self.reps = reps
        self.difficulty_level = difficulty_level
        self.calories_burned = calories_burned

    def skip(self):
        for i in utilities().illustrate_exercise(
            "TrainerImages/skip_illustration.jpeg", "Warm Up"
        ):
            yield (i)

        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        cap = cv2.VideoCapture("TrainerData/woman_skipping.mp4")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level * 2

        while count < total_reps:

            success, img = cap.read()
            is_person_facing_foward = False

            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)

            if len(landmark_list) != 0:
                left_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_arm_angle = detector.find_angle(img, 12, 14, 16)

                left_leg_angle = detector.find_angle(img, 24, 26, 28)
                right_leg_angle = detector.find_angle(img, 23, 25, 27)

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]

                per = np.interp(left_arm_angle, (130, 145), (0, 100))
                bar = np.interp(left_arm_angle, (130, 145), (650, 100))

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_person_facing_front(
                    img, shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]

                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            # cv2.imshow("Skipping", img)
            # cv2.waitKey(1)
        time_elapsed = int(time.process_time() - start)

        # Calorie calculator: Duration (in minutes)*(MET*3.5*weight in kg)/200
        calories_burned = int((time_elapsed / 60) * ((8.0 * 3.5 * 64) / 50))


class simulate_target_exercies:
    def __init__(self, difficulty_level=1, reps=2):
        self.reps = reps
        self.difficulty_level = difficulty_level

    def push_ups(self):
        for i in utilities().illustrate_exercise(
            "TrainerImages/push_up_illustration.jpeg", "PUSH UP'S"
        ):
            yield (i)
        
        cap = cv2.VideoCapture("TrainerData/push_up_right_side.mp4")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                left_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_arm_angle = detector.find_angle(img, 12, 14, 16)

                per = np.interp(right_arm_angle, (60, 140), (0, 100))
                bar = np.interp(right_arm_angle, (60, 140), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_y1 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)

                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_floor_exercise(img, is_person_facing_foward)

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            # cv2.imshow("Push Ups", img)
            # cv2.waitKey(1)
            if count == (self.reps * self.difficulty_level):
                break
            time_elapsed = int(time.process_time() - start)
            calories_burned = (time_elapsed / 60) * ((4.0 * 3.5 * 64) / 200)

    def bicep_curls(self):
        for i in utilities().illustrate_exercise(
            "TrainerImages/bicep_curls_illustration.jpeg", "BICEP CURLS"
        ):
            yield (i)
        
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        cap = cv2.VideoCapture("TrainerData/bicep_curls.mov")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            is_person_facing_foward = False
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            if len(landmark_list) != 0:
                right_arm_angle = detector.find_angle(img, 12, 14, 16)

                per = np.interp(right_arm_angle, (50, 160), (0, 100))
                bar = np.interp(right_arm_angle, (50, 160), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_person_facing_front(
                    img, shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            # cv2.imshow("Image", img)
            # cv2.waitKey(1)

            time_elapsed = int(time.process_time() - start)
            calories_burned = (time_elapsed / 60) * ((4.0 * 3.5 * 64) / 200)

    def mountain_climbers(self):
        for i in utilities().illustrate_exercise(
            "TrainerImages/mountain_climber_illustraion.jpeg", "MOUNTAIN CLIMBERS"
        ):
            yield (i)
        
        cap = cv2.VideoCapture("TrainerData/gym_day_climbers.mov")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()

            print("----------")
            print("----------")
            print("file exists?", os.path.exists("TrainerData/gym_day_climbers.mov"))

            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                left_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_arm_angle = detector.find_angle(img, 12, 14, 16)
                left_leg_angle = detector.find_angle(img, 24, 26, 28)

                right_leg_angle = detector.find_angle(img, 23, 25, 27)

                per = np.interp(right_leg_angle, (220, 280), (0, 100))
                bar = np.interp(right_leg_angle, (220, 280), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_x2 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]

                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_floor_exercise(img, is_person_facing_foward)

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            time_elapsed = int(time.process_time() - start)
            calories_burned = (time_elapsed / 60) * ((4.0 * 3.5 * 64) / 200)

    def squats(self):
        for i in utilities().illustrate_exercise(
            "TrainerImages/squats_illustration.jpeg", "SQUATS"
        ):
            yield (i)
        
        cap = cv2.VideoCapture("TrainerData/gym_day_squats.mov")
        detector = pm.posture_detector()
        count = 0
        direction = 0

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                right_leg_angle = detector.find_angle(img, 24, 26, 28)
                left_leg_angle = detector.find_angle(img, 23, 25, 27)

                per = np.interp(left_leg_angle, (190, 240), (0, 100))
                bar = np.interp(left_leg_angle, (190, 240), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_person_facing_front(
                    img, shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            # cv2.imshow("Squats", img)
            # cv2.waitKey(1)


class start_workout_session:
    def __init__(self, difficulty_level=1):
        self.difficulty_level = difficulty_level

    def completion_screen(self, congrats_img):
        img = cv2.imread(congrats_img)
        ret, jpeg = cv2.imencode(".jpg", img)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
        )
        time.sleep(4)

        # seconds = 3
        # while seconds >= 0:
        #     img = cv2.imread(congrats_img)
        #     img = cv2.resize(img, (980, 550))
        #     ret, jpeg = cv2.imencode(".jpg", img)
        #     yield (
        #         b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + + b"\r\n\r\n"
        #     )

        #     # cv2.imshow("Image", img)
        #     time.sleep(1)
        #     seconds -= 1
        # cv2.waitKey(1)

    def calculate_calories(self, time_elapsed, weight, gender):
        total_calories = 0
        # Met value by exercises
        # Total calories burned = Duration (in minutes)*(MET*3.5*weight in kg)/200
        met_value_by_exercises = {
            "skip": 12.3,
            "bc": 6.0,
            "mc": 8.5,
            "push_ups": 8.0,
            "squats": 5.0,
        }
        if len(weight) != 0:
            weight = weight_in_kg = int(weight) * 0.45359237
        else:
            weight_in_kg = 150

        print(weight)
        print(type(weight))

        for ex, met_value in met_value_by_exercises.items():
            total_calories = float(
                (met_value * 3.5) * (weight_in_kg / 200) * (time_elapsed / 60)
            )

        if gender == "Male":
            total_calories = float(
                total_calories + (total_calories * 0.05) * (time_elapsed / 60)
            )

        return total_calories

    def complete_path(self, difficulty_level, age, weight, gender):
        warm_ups = simulate_warmup(self.difficulty_level)
        target_exercises = simulate_target_exercies(self.difficulty_level)

        skipping_performance = warm_ups.skip()
        squats_performance = target_exercises.squats()
        bicep_curls_performance = target_exercises.bicep_curls()
        mc_performance = target_exercises.mountain_climbers()
        pushup_performance = target_exercises.push_ups()

        print("---------------")
        for i in bicep_curls_performance:
            yield (i)

        for i in mc_performance:
            yield (i)

        for i in pushup_performance:
            yield (i)

        for i in squats_performance:
            yield (i)

        for i in skipping_performance:
            yield (i)

        # return  self.calculate_performance(overall_performance, difficulty_level, age, weight, gender)

        # skipping_performance = warm_ups.skip()

        # simulate_target_exercies.mountain_climbers()
        # simulate_target_exercies.bicep_curls()
        # simulate_target_exercies.push_ups()


def main():
    print("TODO")
    # start_workout_session().complete_path()


if __name__ == "__main__":
    main()
