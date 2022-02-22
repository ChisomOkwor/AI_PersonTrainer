import ExercisesModule as trainer
import EmailingSystem as email_sys
import DatabaseSys as db_sys
import AudioCommSys as audio_sys

from flask import Flask, render_template, Response
from camera import VideoCamera

app= Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template("/index.html")


@app.route('/configure')
def configure():
    return render_template("/configure.html")

def gen_camera(camera):
    while(True):
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed_camera')
def video_feed_camera():
    return Response( gen_camera(VideoCamera()) , mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    while(True):
        # frame = camera.get_frame()
        for i in trainer.start_workout_session(1).complete_path():
            yield i
        # yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    
@app.route('/video_feed')
def video_feed():
    return Response(  gen() , mimetype='multipart/x-mixed-replace; boundary=frame')


# def main():
#     audio_sys.text_to_speech("Are you a registered user? (Enter YES or NO)")
#     existing_user = input("Are you a registered user?(enter y or n): ")
#     if "y" in existing_user.lower():
#         user_email = input("Please enter your registered email: ")
#         first_name = db_sys.authenticate_user(user_email)["first_name"]
#     else:
#         user_reg= db_sys.register_user()
#         first_name = user_reg["first_name"]
#         user_email = user_reg["email"]
#         audio_sys.text_to_speech("You have registered successfully! ")

#     audio_sys.text_to_speech("Hello " + first_name + ". Select a difficulty Level: Easy, Medium or Hard.")
#     difficulty_level = int(input("For easy enter 1, for medium 2, and for hard 3: "))

#     audio_sys.text_to_speech("When you are ready, say READY.")
#     ready = (audio_sys.speech_to_text()).lower()

#     if "ready" in ready:
#         session = trainer.start_workout_session(difficulty_level)
#         performance = session.complete_path()
#         session.completion_screen("/Users/chisom/Desktop/AIproject/TrainerImages/you_rock.jpeg")
#         audio_sys.text_to_speech("Workout complete! You will recieve your stats in your email! You, did it.")
#         email_sys.email_user(user_email, first_name , str(performance["calories"]), performance["time_elapsed"])  

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
    # main()