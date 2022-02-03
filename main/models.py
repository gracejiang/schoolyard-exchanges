from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exchange(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", null=True)
    created_at = models.DateTimeField()
    
    offer_title = models.TextField(max_length=100, default="")
    offer_description = models.TextField(max_length=1000, default="")
    offer_type = models.TextField(default="")
    lf_title = models.TextField(max_length=100, default="")
    lf_description = models.TextField(max_length=1000, default="")
    lf_type = models.TextField(default="")

    def __str__(self):
        return self.body