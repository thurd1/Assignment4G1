from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Shopping', 'Shopping'),
        ('Health', 'Health'),
	('School', 'School'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    due_date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
