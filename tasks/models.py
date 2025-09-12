from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    due_date = models.DateField(default=date.today)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.user.username})"



