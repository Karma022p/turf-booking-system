from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('', views.index, name='index'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('sports_register', views.sports_register, name='sports_register'),
    path('player_register', views.player_register, name='player_register'),
    path('sports_dashboard', views.sports_dashboard, name='sports_dashboard'),
    path('book-sport', views.book_sport, name='book_sport'),
    path('player_dashboard', views.player_dashboard, name='player_dashboard'),
    path('startmatches', views.startmatches, name='startmatches'),
    path('team_a', views.team_a, name='team_a'),
    path('add_players_to_team/', views.add_players_to_team, name='add_players_to_team'),
    path('add_players_to_team_b/', views.add_players_to_team_b, name='add_players_to_team_b'),
    path('set_team_b_session/', views.set_team_b_session, name='set_team_b_session'),
    path('scoreboard', views.scoreboard, name='scoreboard'),
    path('team_b', views.team_b, name='team_b'),
    path('startMatch', views.startMatch, name='startMatch'),
    path('set-selected-team/', views.set_selected_team, name='set_selected_team'),
    # path("create-team/", views.create_team, name="create_team"),
    # path("add-players/<int:team_id>/", views.add_players, name="add_players"),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('update_booking_status/', views.update_booking_status, name='update_booking_status'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('save-payment/', views.save_payment, name='save_payment'),
    path('feedback/', views.feedback_view, name='feedback_view'),
    path('grp/<str:group_name>/', views.grp, name='grp'),
    path('log_in', views.log_in, name='log_in'),
    path("chatbot-response/", views.chatbot_response, name="chatbot_response"),
    path("dynamic_pricing", views.dynamic_pricing, name="dynamic_pricing"),
    path('log_out/', views.log_out, name='log_out'), 
    

]
