
from django.db import models

# Create your models here.


class Magnet(models.Model):
    url = models.CharField(primary_key=True, max_length=255)
    category = models.CharField(max_length=100, null=True)
    title = models.TextField()
    magnet = models.TextField()
    reg_date = models.DateTimeField(db_index=True, auto_now_add=True)

