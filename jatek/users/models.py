from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    ROLE_CHOICES = [
        ('player', 'Játékos'),
        ('gamemaster', 'Játékmester'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"