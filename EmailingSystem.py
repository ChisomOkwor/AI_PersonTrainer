from nylas import APIClient
import datetime
import json
import random

CLIENT_ID = ""
CLIENT_SECRET = ""
ACCESS_TOKEN = ""

nylas = APIClient(
    CLIENT_ID,
    CLIENT_SECRET,
    ACCESS_TOKEN,
)

def email_user(email, name, calories, time):
    today = datetime.date.today()

    # Textual month, day and year	
    today_date = today.strftime("%B %d, %Y")

    time_secs = str(time % 60) + " secs"
    time_mins = str(time // 60) + " mins"
    time_secs_mins = time_mins + ", and  "  + time_secs

    funny_img1 = "TrainerImages/great_job2.jpeg"
    funny_img2 = "TrainerImages/you_rock.jpeg"
    funny_images = [funny_img1, funny_img2]
    random_img = random.randint(0, 2)
    
    attachment = open(funny_images[1], 'rb')
    file = nylas.files.create()
    file.filename = 'complete1.jpg'
    file.stream = attachment
    file.save()
    attachment.close()

    draft = nylas.drafts.create()
    draft.subject = "Performance Summary - From vTrainer"

    # Email message as a strigfied HTML
    greeting = "<p style=\"font-size:30px; text-align: center; color:Red;\"> <b>Amazing Workout " + name + "! </b> </p> <br>"
    performance_summary = "<p style=\"font-size:20px; text-align: center;\"><b>Here is your Performance Summary<b> for "
    date_calories_time =  today_date + ":<br><br> CALORIES BURNED: " + calories + "<br><br> TOTAL WORKOUT TIME: " + time_secs_mins + "</p>"
    
    draft.body =  greeting + performance_summary + date_calories_time 
    draft.to = [{'name': name, 'email': email}]  
    draft.attach(file)
    draft.send()

def main():  
    # Test Emailing
    email_user("okwor@gmail.com", "Chisom", "80", 100)

if __name__ == "__main__":
    main()
