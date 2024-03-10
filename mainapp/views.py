from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import credentials,db,auth
import os
import pyrebase
import requests

config = {
  'apiKey': "AIzaSyDG8BHCUT0yUr4qobBaWTU2dWt6iLOdrhM",
  'authDomain': "cybermazearena-c54ff.firebaseapp.com",
  'databaseURL': "https://console.firebase.google.com/u/0/project/cybermazearena-c54ff/database/cybermazearena-c54ff-default-rtdb/data/~2F",  # Add this line
  'projectId': "cybermazearena-c54ff",
  'storageBucket': "cybermazearena-c54ff.appspot.com",
  'messagingSenderId': "985558326455",
  'appId': "1:985558326455:web:4d9d19cb293ccd6d314132",
  'measurementId': "G-WKEX8CHQV3"
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

cred = credentials.Certificate('mainapp\private-key.json')
firebase_admin.initialize_app(cred)

def loading(request):
    return render(request, "index.html")

def mainpage(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})# Adjust the redirect URL as needed

    # If Firebase authentication is successful, render the main page
    return render(request, "main.html")

def is_email_registered(email):
    try:
        user_list = auth.list_users() 
        for user in user_list.users:
            if user.email == email:
                return True
    except Exception as e:
        # Handle exceptions
        return False


def signIn(request):
    return render(request, "login.html")

def signUp(request):
    return render(request,"signup.html")

def home(request):
    return render(request,"homepage.html")

def postsignIn(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        # Sign in the user with the given email and password
        user = authe.sign_in_with_email_and_password(email, passw)
        # Get user's ID token from Firebase
        session_id = user['idToken']
        # Set user's ID token in session
        request.session['uid'] = str(session_id)
        # Redirect to main page
        return redirect('main')
    except Exception as e:
        print("Firebase Authentication Error:", e)
        message = "Invalid Credentials!! Please Check your Data"
        return render(request, "Login.html", {"message": message})


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")

import requests

def create_user_with_email_and_password(email, password):
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyDG8BHCUT0yUr4qobBaWTU2dWt6iLOdrhM'
    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    response = requests.post(url, json=payload)
    data = response.json()
    if 'idToken' in data:
        # User creation successful, return user's ID token
        return data['idToken']
    else:
        # User creation failed, handle error
        error_message = data['error']['message']
        return None

def store_user_details_in_database(user_id, email, name, dob):
    # Construct the URL for your Realtime Database
    url = f'https://YOUR_PROJECT_ID.firebaseio.com/users/{user_id}.json'
    user_data = {
        'email': email,
        'name': name,
        'dob': dob
    }
    response = requests.put(url, json=user_data)
    if response.ok:
        # Data stored successfully
        return True
    else:
        # Error storing data
        return False

def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    conpass = request.POST.get("conpass")
    name = request.POST.get('name')
    dob = request.POST.get('dob')
    
    try:
        if is_email_registered(email) is True:
            message = "EmailID Already Exists, Try Another EmailID"
            return render(request, "login.html", {"message": message}) 
        else:
            if passs == conpass:
                # Create user with email and password
                user = auth.create_user_with_email_and_password(email, passs)
                
                # Get the user's ID from the response
                user_id = user['localId']
                
                # Store additional user details in the Realtime Database
                user_data = {
                    'username': name,
                    'email': email,
                    'dob': dob
                }
                
                # Path to store user data in the database (adjust as per your database structure)
                user_ref = database.child('users').child(user_id)
                
                # Push user data to the database
                user_ref.set(user_data)
                
                # Retrieve user data from the database
                matching_user = user_ref.get().val()
                
                # Redirect to main page with user details
                return render(request, "main.html", {'matching_user': matching_user})
            else:
                message = "Password and confirm Password Don't Match! Please Check"
                return render(request, "signup.html", {"message": message})
    except Exception as e:
        print(e)
        return render(request, "signup.html")

def reset(request):
	return render(request, "reset.html")

def postReset(request):
    email = request.POST.get('email')
    try:
        # Firebase Auth REST API endpoint for password reset
        reset_endpoint = f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=AIzaSyDG8BHCUT0yUr4qobBaWTU2dWt6iLOdrhM'

        # Payload for the password reset request
        payload = {
            'requestType': 'PASSWORD_RESET',
            'email': email,
        }

        # Make a POST request to the Firebase Auth REST API
        response = requests.post(reset_endpoint, json=payload)

        if response.ok:
            message = "An email to reset the password has been sent."
            return render(request, "reset.html", {"msg": message})
        else:
            error_message = "Something went wrong. Please check the email provided or try again later."
            return render(request, "reset.html", {"msg": error_message})

    except Exception as e:
        print(e)
        message = "Something went wrong. Please check the email you provided is registered or not."
        return render(request, "reset.html", {"msg": message})


def blog_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, 'blogs.html')


def hta_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, './blogs/howtoseries/howtoapproach.html')


def crypto_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "./blogs/howtoseries/crypto.html")


def forensics_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "./blogs/howtoseries/forensics.html")


def pwn_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "./blogs/howtoseries/pwn.html")


def reversing_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "./blogs/howtoseries/reversing.html")


def osint_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "./blogs/howtoseries/osint.html")


def stegano_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})
        
    return render(request, "./blogs/howtoseries/steganography.html")


def web_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "./blogs/howtoseries/web.html")


def gitlab_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "./blogs/gitlab2023/index.html")


def chrome_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "./blogs/chrome2023/index.html")


def learn_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "learn.html")


def guided_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})

    return render(request, "./learn/guided/guided.html")


def practice_view(request):
    firebase_user = None
    try:
        firebase_user = auth.verify_id_token(request.session['uid'])
    except Exception as e:
        print(e)
        # Redirect to login page if Firebase authentication fails
        message = "Not Authorized"
        return render(request, "Login.html", {"message": message})
        
    return render(request, "./learn/practice/practice.html")

def verify_flag(request):
    if request.method == 'POST':
        flag = request.POST.get('flag')
        if flag == 'ACNCTF{appreciation.laughably.subdue}':  # Replace with your actual flag
            success_message = "Congratulations! Flag is correct."
            return render(request, './learn/guided/guided.html', {'success_message': success_message})
        else:
            error_message = "Flag is incorrect. Please try again."
            return render(request, './learn/guided/guided.html', {'error_message': error_message})
    else:
        return render(request, 'error.html')

def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})