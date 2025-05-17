from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models,connection
# Create your models here.
# Create your models here.
class Sport_Club(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  
    repassword = models.CharField(max_length=100)  
    pincode = models.CharField(max_length=100)  
    country = models.CharField(max_length=100)  
    state = models.CharField(max_length=100)  
    city = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.name} from {self.city}"
    

class Player_Details(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    repassword = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} from {self.city}"
    


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Booked', 'Booked'),
        ('Rejected', 'Rejected'),
    ]

    player_name = models.CharField(max_length=100)
    no_of_players = models.IntegerField()
    game_type = models.CharField(max_length=50)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    ending_time = models.TimeField()
    no_of_hours = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sports_club = models.ForeignKey(Sport_Club, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'  # Default status
    )
    
    def __str__(self):
        return f"Booking for {self.player_name} at {self.sports_club.name} ({self.status})"
    


class Payment(models.Model):
    player_name = models.CharField(max_length=100)
    sports_name = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_slip = models.FileField(upload_to='payment_slips/')

    def __str__(self):
        return self.player_name
    
class Feedback(models.Model):
    player = models.CharField(max_length=100)
    sports = models.CharField(max_length=100)
    feedback_text = models.TextField()
    rating = models.IntegerField()  # New field to store the predicted rating

    def __str__(self):
        return f"Feedback from {self.player} for {self.sports}"


class Message(models.Model):
    sender = models.CharField(max_length=100)  # Player Name
    message = models.TextField()  # Message content
    group = models.CharField(max_length=100)  # Group name
    time = models.DateTimeField(default=now)  # Message time

    def __str__(self):
        return f"{self.sender} -> {self.group} at {self.time}"



class TeamA(models.Model):
    ateamName = models.CharField(max_length=255)
    ateamCity = models.CharField(max_length=100)
    acaptainName = models.CharField(max_length=255)
    players = models.ManyToManyField(Player_Details, related_name='teams') 
    date_time = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ateamName} from {self.ateamCity}"

class TeamB(models.Model):
    teamName = models.CharField(max_length=100, unique=True)
    teamCity = models.CharField(max_length=100)
    captainNumber = models.CharField(max_length=15)  
    captainName = models.CharField(max_length=100)
    players = models.ManyToManyField(Player_Details)
    date_time2 = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.teamName} from {self.teamCity}"
    
    
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def create_ground_table(self):
        with connection.cursor() as cursor:
            table_name = f'ground_{self.name.lower()}'
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    ground_name VARCHAR(100) NOT NULL
                )
            ''')

    def __str__(self):
        return self.name

class Ground(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.city.create_ground_table()
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return f"{self.name} from {self.city}"
    


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    

class Players_added_to_team_a(models.Model):
    team = models.ForeignKey(TeamA, on_delete=models.CASCADE)
    player = models.ForeignKey(Player_Details, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'player')  # This prevents duplicate entries
        verbose_name = "Player Added to Team A"
        verbose_name_plural = "Players Added to Team A"

    def __str__(self):
        return f"{self.player.name} added to {self.team.ateamName}"
    
    
class Players_added_to_team_b(models.Model):
    team = models.ForeignKey(TeamB, on_delete=models.CASCADE)
    player = models.ForeignKey(Player_Details, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'player')  # This prevents duplicate entries
        verbose_name = "Player Added to Team B"
        verbose_name_plural = "Players Added to Team B"

    def __str__(self):
        return f"{self.player.name} added to {self.team.teamName}"