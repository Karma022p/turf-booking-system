from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .auth import authentication
from .models import Sport_Club, Player_Details,Booking,Payment,Feedback,TeamA,TeamB,City,Ground,Players_added_to_team_a,Players_added_to_team_b
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Message
from django.utils.timezone import now

# Create your views here.
def index(request):
    return render(request, 'index.html')

def scoreboard(request):
    # Get selected team from session storage (passed from startMatch)
    selected_team = request.session.get('selected_team')
    
    # Initialize variables
    team_name = ""
    team_players = []
    
    if selected_team == request.session.get('team_a_name'):
        # Team A was selected
        team_id = request.session.get('team_a_id')
        team_name = request.session.get('team_a_name')
        if team_id:
            try:
                player_entries = Players_added_to_team_a.objects.filter(team_id=team_id)
                unique_players = set()
                for entry in player_entries:
                    player_data = {
                        'id': entry.player.id,
                        'name': entry.player.name
                    }
                    if player_data['id'] not in unique_players:
                        unique_players.add(player_data['id'])
                        team_players.append(player_data)
            except Exception as e:
                print(f"Error fetching Team A players: {e}")
    else:
        # Team B was selected
        team_id = request.session.get('team_b_id')
        team_name = request.session.get('team_b_name')
        if team_id:
            try:
                player_entries = Players_added_to_team_b.objects.filter(team_id=team_id)
                unique_players = set()
                for entry in player_entries:
                    player_data = {
                        'id': entry.player.id,
                        'name': entry.player.name
                    }
                    if player_data['id'] not in unique_players:
                        unique_players.add(player_data['id'])
                        team_players.append(player_data)
            except Exception as e:
                print(f"Error fetching Team B players: {e}")
    
    return render(request, 'scoreboard.html', {
        'team_name': team_name,
        'team_players': team_players[:2]  # Only take first 2 players
    })
    
    
def set_selected_team(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['selected_team'] = data.get('selected_team')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)   
    
    
def startMatch(request):
    # Get team names from session or set defaults
    team_a_name = request.session.get('team_a_name', 'Team A Not Selected')
    team_b_name = request.session.get('team_b_name', 'Team B Not Selected')
    
    return render(request, 'startMatch.html', {
        'team_a_name': team_a_name,
        'team_b_name': team_b_name,
        'fname': request.user.first_name,
        'lname': request.user.last_name
    })

def startmatches(request):
    return render(request, 'startmatches.html')

def team_a(request):
    if request.method == "POST":
        teamName = request.POST.get('teamName')
        teamCity = request.POST.get('teamCity')
        captainNumber = request.POST.get('captainNumber')
        captainName = request.POST.get('captainName')

        try:
            team_a = TeamA(
                ateamName=teamName,
                ateamCity=teamCity,
                acaptainName=captainName
            )
            team_a.save()
            messages.success(request, "Team A has been added successfully.")
            return redirect('team_a')
        except Exception as e:
            messages.error(request, f"Error creating team: {str(e)}")
            return redirect('team_a')

    teams_a = TeamA.objects.all()
    players = Player_Details.objects.all()
    
    return render(request, 'team_a.html', {
        'teams_a': teams_a,
        'players': players,
        'fname': request.user.first_name,
        'lname': request.user.last_name
    })


@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def team_b(request):
    teams_b = TeamB.objects.all()
    players = Player_Details.objects.all()
    
    context = {
        'fname': request.user.first_name,
        'lname': request.user.last_name,
        'teams_b': teams_b,
        'players': players
    }

    if request.method == "POST":
        # Check if this is a team selection
        if 'selected_team_id' in request.POST:
            team_id = request.POST.get('selected_team_id')
            try:
                team = TeamB.objects.get(id=team_id)
                request.session['team_b_id'] = team_id
                request.session['team_b_name'] = team.teamName
                return redirect('startMatch')
            except TeamB.DoesNotExist:
                messages.error(request, "Selected team not found")
                return redirect('team_b')
        
        # Existing team creation code
        teamName = request.POST.get('teamName')
        teamCity = request.POST.get('teamCity')
        captainNumber = request.POST.get('captainNumber')
        captainName = request.POST.get('captainName')

        team_b = TeamB(
            teamName=teamName,
            teamCity=teamCity,
            captainNumber=captainNumber,
            captainName=captainName
        )
        team_b.save()

        messages.success(request, "Team B has been added successfully.")
        return redirect('team_b')

    return render(request, 'team_b.html', context)

def sports_dashboard(request):
    current_user = request.user
    try:
        # Fetch the sports club related to the current user
        sports_club = Sport_Club.objects.get(username=current_user.username)
        
        # Use the name or relevant field from sports_club to filter feedback
        feed = Feedback.objects.filter(sports=sports_club.name)  # Replace `name` with the correct field
        pay =  Payment.objects.filter(sports_name=sports_club.name)
        # Fetch booking details for the sports club
        booking_details = Booking.objects.filter(sports_club=sports_club)
    except Sport_Club.DoesNotExist:
        feed = []  # If no sports club found, set feedback to an empty list
        booking_details = []
        pay = []

    context = {
        'booking_details': booking_details,  # Fetch booking data
        'feed': feed,  # Fetch feedback for the logged-in sports club
        'pay':pay
    }
    return render(request, 'sports_dashboard.html', context)


def player_dashboard(request):
    # Fetch the logged-in player's full name
    player_name = request.user.get_full_name()  # Or use request.user.first_name for just the first name

    if request.method == 'POST':
        # Get form data from POST request
        no_of_players = request.POST.get('no_of_players')
        game_type = request.POST.get('game_type')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        ending_time = request.POST.get('ending_time')
        no_of_hours = request.POST.get('no_of_hours')
        amount = request.POST.get('amount')
        sports_club_id = request.POST.get('sports_club')

        # Fetch the selected sports club based on the ID
        sports_club = Sport_Club.objects.get(id=sports_club_id)

        # Save the booking details
        booking = Booking(
            player_name=player_name,
            no_of_players=no_of_players,
            game_type=game_type,
            booking_date=booking_date,
            booking_time=booking_time,
            ending_time=ending_time,
            no_of_hours=no_of_hours,
            amount=amount,
            sports_club=sports_club,
        )
        booking.save()

        # Success message
        messages.success(request, "Your booking has been successfully submitted!")

        return redirect('player_dashboard')

    # Fetch all turfs, feedback, and booking details for the player
    turf = Sport_Club.objects.all()
    fd = Feedback.objects.all()
    book_details = Booking.objects.filter(player_name=player_name)
    player2=Player_Details.name
    # Pass context to the template
    context = {
        'player_name': player_name,  # Add player_name to the context
        'turf': turf,
        'book_details': book_details,
        'fd': fd,
        
    }

    # Render the player_dashboard template
    return render(request, 'player_dashboard.html', context)


def book_sport(request, sports_id):
    if request.method == 'POST':
        player_name = request.POST['player_name']
        no_of_players = request.POST['no_of_players']
        game_type = request.POST['game_type']
        booking_date = request.POST['booking_date']
        booking_time = request.POST['booking_time']
        ending_time = request.POST['ending_time']
        no_of_hours = request.POST['no_of_hours']
        amount = request.POST['amount']
        

        booking = Booking.objects.create(
            player_name=player_name,
            no_of_players=no_of_players,
            game_type=game_type,
            booking_date=booking_date,
            booking_time=booking_time,
            ending_time=ending_time,
            no_of_hours=no_of_hours,
            amount=amount
        )
        booking.save()
        messages.success(request, "Your booking has been successfully submitted!")

        return redirect('book_sport', sports_id=sports_id)

    return render(request, 'player_dashboard.html', {'sports_id': sports_id})


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password') 

        if username == 'admin@gmail.com' and password == 'admin@123':
            admin_user, created = User.objects.get_or_create(username='admin@gmail.com', email='admin@gmail.com')
            admin_user.set_password('admin@123')
            admin_user.save()

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Log In Successful...!")
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Invalid User...!")
                return redirect("admin_login")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("admin_login")

    return render(request, "admin_login.html", {'action': 'admin_login'})


def log_in(request):
    if request.method == "POST": 
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if Sport_Club.objects.filter(username=username).exists():
                messages.success(request, "Log In Successful! Redirecting to your sports club dashboard.")
                return redirect("sports_dashboard")

            elif Player_Details.objects.filter(email=username).exists():
                messages.success(request, "Log In Successful! Redirecting to your player dashboard.")
                return redirect("player_dashboard")

            messages.success(request, "Log In Successful! Redirecting to the admin dashboard.")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid Username or Password.")
            return redirect("log_in")

    return render(request, "log_in.html", {'action': 'log_in'})



def sports_register(request):
    if request.method == "POST":
        name = request.POST.get('club_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('confirm_password')
        pincode = request.POST.get('pincode')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')

        if password != repassword:
            messages.error(request, "Passwords do not match!")
            return redirect("sports_register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("sports_register")

        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.save()

        sport_club = Sport_Club(
            name=name,
            username=username,
            password=password,  
            repassword=repassword, 
            pincode=pincode,
            country=country,
            state=state,
            city=city
        )
        sport_club.save()

        messages.success(request, "Your account has been created successfully.")
        return redirect("log_in")

    return render(request, "sports_register.html")

@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    sports_book = Booking.objects.all()
    player_data = Player_Details.objects.all()
    sports_data = Sport_Club.objects.all()
    context = {'sports_book': sports_book, 'player_data': player_data, 'sports_data': sports_data}
    return render(request, 'admin_dashboard.html', context)

def player_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username') 
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("player_register")

        if Player_Details.objects.filter(email=username).exists():
            messages.error(request, "Email already exists!")
            return redirect("player_register")

        player_details = Player_Details(
            name=name,
            email=username,
            password=password,
            repassword=confirm_password,
            phone=phone,
            pincode=pincode,
            country=country,
            state=state,
            city=city
        )
        player_details.save()

        user = User.objects.create_user(
            username=username,
            password=password,
            email= password,
            first_name = name
            
        )
        user.save()


        messages.success(request, "Player account has been created successfully.")
        return redirect("log_in")

    return render(request, 'player_register.html')





@csrf_exempt 
def update_booking_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            booking_id = data.get('booking_id')
            status = data.get('status')

            if not booking_id or not status:
                return JsonResponse({'success': False, 'error': 'Invalid data'})

            booking = Booking.objects.get(id=booking_id)
            booking.status = status
            booking.save()

            return JsonResponse({'success': True, 'status': status})
        except Booking.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Booking not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.delete()

    messages.success(request, 'Booking deleted successfully!')

    return redirect('admin_dashboard')  

@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("/")



# def save_payment(request):
#     if request.method == 'POST':
#         player_name = request.POST.get('player_name')
#         amount = request.POST.get('amount')
#         payment_slip = request.FILES.get('payment_slip')

#         payment = Payment(player_name=player_name, amount=amount, payment_slip=payment_slip)
#         payment.save()

#         return JsonResponse({'message': 'Payment saved successfully!'})
#     return JsonResponse({'error': 'Invalid request'}, status=400)

def save_payment(request):
    if request.method == "POST":
        player_name = request.POST.get('player_name')
        sports_name = request.POST.get('sports_name')  # Get sports name from the form
        amount = request.POST.get('amount')
        payment_slip = request.FILES.get('payment_slip')

        # Check if required fields are provided
        if not player_name or not sports_name or not amount or not payment_slip:
            return JsonResponse({'error': 'All fields are required!'})

        # Save the payment details including sports name
        payment = Payment(player_name=player_name, sports_name=sports_name, amount=amount, payment_slip=payment_slip)
        payment.save()

        return JsonResponse({'message': 'Payment recorded successfully!'})

    return JsonResponse({'error': 'Invalid request method.'})
    

plt=Player_Details.name
print(plt)


# @login_required(login_url="log_in")
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def feedback_view(request):
   
#     if request.method == 'POST':
#         sports = request.POST.get('sportsSelect')
#         feedback_text = request.POST.get('feedbackTextarea')
        
#         # Save the feedback data to the Feedback model
#         feedback = Feedback(sports=sports, feedback_text=feedback_text, player=request.user.first_name)
#         feedback.save()

#         messages.success(request, 'Feedback submitted successfully!')
#         return redirect('player_dashboard')  # Adjust as necessary

#     return render(request, 'player_dashboard.html')



@login_required
def grp(request, group_name):
    # Get the name of the logged-in player
    sender_name = request.user.first_name  # Fetch the logged-in user's first name

    if request.method == "POST":
        # Get the message content from the form
        message_content = request.POST.get("message")
        if message_content:
            # Save the message in the database for the selected group
            Message.objects.create(
                sender=sender_name,
                message=message_content,
                group=group_name,  # Save the group name
                time=now(),
            )
            return JsonResponse({"success": True, "message": "Message sent successfully!"})
        else:
            return JsonResponse({"success": False, "message": "Message content is required!"})

    # Fetch all messages for the selected group
    messages = Message.objects.filter(group=group_name).order_by("time")
    return render(request, "grp.html", {
        "messages": messages,
        "group_name": group_name,
        "sender_name": sender_name,
    })


import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Feedback

# Load the trained model and vectorizer
with open("dataset/feedback_predict.pkl", "rb") as f:
    model = pickle.load(f)

with open("dataset/feedback_vectorizer.pkl", "rb") as f:
    vector = pickle.load(f)

# Download stopwords if not already present
nltk.download('stopwords')

# Initialize NLP tools
stop_words = stopwords.words('english')
stemmer = PorterStemmer()

# Preprocess function
def preprocess(text):
    text = text.replace("<br />", " ")  # Remove unnecessary characters
    text = text.lower()  # Convert to lowercase
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedback_view(request):
    if request.method == 'POST':
        sports = request.POST.get('sportsSelect')
        feedback_text = request.POST.get('feedbackTextarea')

        # Predict feedback rating
        processed_feedback = preprocess(feedback_text)
        feedback_vectorized = vector.transform([processed_feedback])
        predicted_rating = model.predict(feedback_vectorized)[0]  # Get the predicted rating

        # Save feedback with rating
        feedback = Feedback(
            sports=sports,
            feedback_text=feedback_text,
            player=request.user.first_name,
            rating=predicted_rating  # Store predicted rating
        )
        feedback.save()

        messages.success(request, 'Feedback submitted successfully!')
        return redirect('player_dashboard')  # Adjust as necessary

    return render(request, 'player_dashboard.html')

from django.urls import reverse
def add_players_to_team(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            team_id = data.get('team_id')
            player_ids = data.get('player_ids')
            
            team = TeamA.objects.get(id=team_id)
            
            # Clear existing players from both ManyToMany and our new table
            team.players.clear()
            Players_added_to_team_a.objects.filter(team=team).delete()
            
            # Add players to both the ManyToMany relationship and our new table
            for player_id in player_ids:
                player = Player_Details.objects.get(id=player_id)
                team.players.add(player)
                # Add to our new tracking table
                Players_added_to_team_a.objects.create(team=team, player=player)
            
            # Store Team A in session
            request.session['team_a_id'] = team_id
            request.session['team_a_name'] = team.ateamName
            
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('team_b')
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)




def add_players_to_team_b(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            team_id = data.get('team_id')
            player_ids = data.get('player_ids')

            if not team_id or not player_ids:
                return JsonResponse({'success': False, 'message': 'Missing team_id or player_ids'}, status=400)

            team = TeamB.objects.get(id=team_id)
            players = Player_Details.objects.filter(id__in=player_ids)
            
            # Add players to the team through ManyToMany relationship
            team.players.add(*players)
            
            # Create records in Players_added_to_team_b table
            for player in players:
                Players_added_to_team_b.objects.create(team=team, player=player)
            
            # Store Team B in session
            request.session['team_b_id'] = team_id
            request.session['team_b_name'] = team.teamName
            request.session.save()  # Explicitly save the session

            return JsonResponse({
                'success': True,
                'redirect_url': reverse('startMatch')
            })
        
        except TeamB.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Team not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

def set_team_b_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            team_id = data.get('team_id')
            
            if not team_id:
                return JsonResponse({'success': False, 'message': 'Missing team_id'}, status=400)

            team = TeamB.objects.get(id=team_id)
            request.session['team_b_id'] = team_id
            request.session['team_b_name'] = team.teamName

            return JsonResponse({
                'success': True,
                'message': 'Team B session set successfully'
            })
        
        except TeamB.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Team not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


import os
import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

os.environ["GOOGLE_API_KEY"] = "AIzaSyDDw4i32pQfN9gRlRAI5JFEg-hzjzlIpLI"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@csrf_exempt  # Remove this if CSRF protection is handled
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").strip()

            if not message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # Generate response using Google Gemini AI
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(message + " Give answer in 50 to 100 words.")

            return JsonResponse({"response": response.text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)



import joblib
import pandas as pd
from django.shortcuts import render

# Load model and encoders once (to avoid reloading them for every request)
model = joblib.load('dataset/ml/price_prediction_model.pkl')
label_encoders = joblib.load('dataset/ml/label_encoders.pkl')

def dynamic_pricing(request):
    predicted_price = None  # Default value

    if request.method == 'POST':
        # Get user input from the form
        user_input = {
            'Day Time': request.POST.get('day_time'),
            'Season': request.POST.get('season'),
            'Time Slot': request.POST.get('time_slot'),
            'Weather': request.POST.get('weather'),
            'Day Type': request.POST.get('day_type'),
            'Special Event': request.POST.get('special_event'),
            'Turf Quality': request.POST.get('turf_quality'),
            'Location Demand': int(request.POST.get('location_demand'))
        }

        # Encode categorical values
        for col in label_encoders:
            if user_input[col] in label_encoders[col].classes_:
                user_input[col] = label_encoders[col].transform([user_input[col]])[0]
            else:
                user_input[col] = 0  # Handle unknown category by assigning default value

        # Convert to DataFrame
        input_df = pd.DataFrame([user_input])

        # Predict price
        predicted_price = model.predict(input_df)[0]

    return render(request, 'dynamic_pricing.html', {'predicted_price': predicted_price})
