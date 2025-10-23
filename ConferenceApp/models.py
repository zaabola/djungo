from django.db import models
from django.core.validators import MinLengthValidator 
from django.core.exceptions import ValidationError
# Create your models here.
class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    description=models.TextField(validators=[
        MinLengthValidator(limit_value=30,
                           message="la description doit contenir au minimum 30 caractéres")
    ])
    location=models.CharField(max_length=255)
    THEME= [
        ("CS&IA","Computer science & IA"),
        ("CS","Social science"),
        ("SE","Science and eng")
    
    ]
    theme=models.CharField(max_length=255,
                            choices=THEME)
    start_date = models.DateField()
    end_date =models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("la date de début de la conférence doit être antérieur") 
class Submission(models.Model):
    submission_id=models.CharField(primary_key=True,max_length=255,unique=True)
    user=models.ForeignKey("UserApp.User",
                           on_delete=models.CASCADE,
                           related_name="submissions")
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="submissions")
    title=models.CharField(max_length=255)
    abstract=models.TextField()
    keywords=models.TextField()
    paper=models.FileField(
        upload_to="papers/"
    )
    CHOICES=[
        ("submitted","submitted"),
        ("under review","under review"),
        ("accepted","accepted"),
        ("rejected","rejected")

    ]
    status=models.CharField(max_length=255,choices=CHOICES)
    payed=models.BooleanField(default=False)
    submission_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)