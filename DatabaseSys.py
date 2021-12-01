import json

def register_user():
    user_info_db = '/Users/chisom/Documents/Senior Seminar/PoseDetection/user_data.json'
    first_name = input("Please Enter your First Name:")
    last_name = input("Please Enter your Last Name:")
    email = input("Please Enter your Email:")
    user_personal_data = { email:{"first_name": first_name, "last_name": last_name} }

    with open(user_info_db,'r') as f:
        dic = json.load(f)
        dic.update(user_personal_data)

    with open(user_info_db, 'w') as f:
        json.dump(dic, f, indent=4)

    return({"first_name": first_name, "email": email})

def authenticate_user(email):
    user_info_db = '/Users/chisom/Documents/Senior Seminar/PersonalTrainer/user_data.json'
    user_is_registered = False
    with open(user_info_db,'r') as f:
        dic = json.load(f)

    while user_is_registered == False:
        if email in dic:
            user_is_registered = True
        else:
            print("EMAIL NOT FOUND. Please regiser. ")
            register_user()
    return(dic[email])
