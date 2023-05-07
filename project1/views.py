import base64

from django.http import HttpResponse, request
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from pymongo import MongoClient
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import  make_password
import hashlib

def index(request):
    return render(request, 'Home.html')


def about(request):
    request.session.modified = True
    return render(request, 'About.html')


def contactus(request):
    request.session.modified = True
    return render(request, 'ContactUs.html')


# def sign_up(request):
#     if request.method == 'POST':
#         form = request.POST.dict()
#         username = form['fname']
#         lastname = form['lname']
#         password = form['pass']
#         email = form['email']
#         client = MongoClient('mongodb://localhost:27017/')
#         db = client['Client']
#         collection = db['users']
#         collection.insert_one({'username': username,'lastname':lastname,'password': password, 'email': email})
#         return redirect('Login.html')
#     else:
#         form = {}
#     return render(request, 'SignUp.html', {'form': form})

from django.shortcuts import render, redirect
from pymongo import MongoClient
from django.http import HttpResponse
import random


# def sign_up(request):
#     if request.method == 'POST':
#         form = request.POST.dict()
#         username = form['fname']
#         lastname = form['lname']
#         password = form['pass']
#         email = form['email']
#         user_type = form['user_type']
#
#         client = MongoClient('mongodb://localhost:27017/')
#         db = client['Client']
#         collection = db['users']
#
#         # Check if the user_type is "influencer"
#         if user_type == "influencer":
#             # phone_number = form['phone_number']
#             # otp = str(random.randint(100000, 999999))
#             # # Generate and verify OTP for the influencer
#             # # You can use a third-party service to send OTP via SMS or email
#             # # Here, we will just print the OTP to the console
#             # print("OTP for phone number", phone_number, "is:", otp)
#             collection.insert_one({'username': username, 'lastname': lastname, 'password': password, 'email': email,
#                                    'user_type': user_type})# 'phone_number': phone_number})
#         else:
#             collection.insert_one({'username': username, 'lastname': lastname, 'password': password, 'email': email,
#                                    'user_type': user_type})
#
#         return redirect('SignUp.html')
#     else:
#         form = {}
#     return render(request, 'SignUp.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = request.POST.dict()
        username = form['fname']
        lastname = form['lname']
        password = form['pass']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        email = form['email']
        user_type = form['user_type']

        client = MongoClient('mongodb://localhost:27017/')
        db = client['Client']
        collection = db['users']

        # Check if the user_type is "influencer"
        if user_type == "influencer":
            collection.insert_one({'username': username, 'lastname': lastname, 'password': hashed_password, 'email': email, 'user_type': user_type})
        else:
            collection.insert_one({'username': username, 'lastname': lastname, 'password': hashed_password, 'email': email, 'user_type': user_type})

        # Save the user in the Django model
        # user = User(first_name=username, last_name=lastname, password=password, email=email)
        # user.save()
        return render(request,'Home.html')
    else:
        form = {}
    return render(request, 'SignUp.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        user_type = request.POST.get('user_type')
        hashed_login_password = hashlib.sha256(password.encode()).hexdigest()
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Client']
        collection = db['users']
        user_data = collection.find_one({'email': email})
        if user_data is not None:
            if user_data['password'] == hashed_login_password and user_data['user_type'] == user_type:
                request.session['username'] = user_data['username'] # add username to session
                if user_type == "influencer":
                    return redirect('iprofile')
                else:
                    return redirect('profile')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'Login.html')

# def log_in(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('pass')
#         user_type = request.POST.get('user_type')
#         client = MongoClient('mongodb://localhost:27017/')
#         db = client['Client']
#         collection = db['users']
#         user_data = collection.find_one({'email': email})
#         if user_data is not None:
#             if user_data['password'] == password and user_data['user_type'] == user_type:
#                 if user_type== 'user':
#                     request.session['username'] = user_data['username'] # add username to session
#                     return redirect('profile')
#                 else:
#                     request.session['username']= user_data['username']
#                     return redirect('iprofile')
#             else:
#                 messages.error(request, 'Invalid email or password')
#         else:
#             messages.error(request, 'Invalid email or password')
#     return render(request, 'Login.html')

@login_required
def log_out(request):
    auth_logout(request)
    request.session.flush()
    return redirect('index')

def smm(request):
    return render(request, 'SocialMediaManagement.html')


def pricing(request):
    return render(request, 'pricing.html')

# @login_required
def profile(request):
    username = request.session.get('username') # retrieve username from session
    return render(request, 'profile.html', {'username': username})


from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
import base64


def yourads(request):
    username = request.session.get('username')
    print(username)
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Client']
    collection = db['ads']
    # Fetch the ads from the database
    ads = collection.find({'username': username})
    # Convert image data to base64 for rendering in the template
    # for ad in ads:
    #     if 'image' in ad:
    #         image_data = ad['image']
    #         ad['image'] = base64.b64encode(image_data).decode('utf-8')
    #         print(image_data)

    return render(request, 'yourads.html', {'ads': ads})


def iprofile(request):
    username = request.session.get('username') # retrieve username from session
    return render(request, 'iprofile.html', {'username': username})



from pymongo import MongoClient
from django.shortcuts import render, redirect

def uploadadd(request):
    influencers = []
    if request.method == 'POST':
        form = request.POST.dict()
        # Save the uploaded image to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Client']
        collection = db['ads']
        username = request.session.get('username')
        mediaType = form['mediaType']
        if mediaType == "image":
            image = request.FILES['image']
            title = form['title']
            description = form['description']
            type = form['platform']
            collection.insert_one({'image': image.read(), 'username': username, 'title': title, 'description': description, 'type': type})
        else:
            url = form['url']
            title = form['title']
            description = form['description']
            type = form['platform']
            collection.insert_one({'url': url, 'username': username, 'title': title, 'description': description, 'type': type})

        # Retrieve usernames of influencers from db['users']
        influencer_collection = db['users']
        influencers = list(influencer_collection.find({'user_type': 'influencer'}))
        print(influencers)
        return redirect('profile')  # Render a success page after upload
    return render(request, 'uploadadd.html', {'influencers': influencers})  # Render the upload form initially


def iyouradds(request):
    username = request.session.get('username')
    print(username)
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Client']
    collection = db['ads']
    # Fetch the ads from the database
    ads = collection.find({'type': "youtube" }) 
    # Convert image data to base64 for rendering in the template
    # for ad in ads:
    #     if 'image' in ad:
    #         image_data = ad['image']
    #         ad['image'] = base64.b64encode(image_data).decode('utf-8')
    #         print(image_data)

    return render(request, 'ads.html', {'ads': ads})

# def add_add(request):
#     request.session.modified = True
#     new={"image":"this is image","Description":"this is all about image"}
#     email="goutham@gmail.com"
#     doc=client_details.find_one({'Email':email})
#     if doc:
#         user_id = doc['_id']
#         client_details.update_one({'_id': user_id}, {'$push': {'client_adds': new}})
#         return HttpResponse("success")
#     else:
#         return HttpResponse('failed')

# def addimg(request):
#


def imgup(request):
    return render(request, 'profile.html', {
        "im": "https://media.istockphoto.com/id/1158358904/photo/spraying-perfume-on-dark-background-closeup-image.jpg?s=612x612&w=0&k=20&c=FgO1tJIxW_fVH0e7YHb-oMb_iDshELnMR6qXGILQFcU="})
