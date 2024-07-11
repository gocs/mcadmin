from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='general.log', level=logging.INFO)

# Create your models here.
class Player(models.Model):
    id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AbstractPayment(models.Model):
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Payment(AbstractPayment):
    def __str__(self):
        return self.player.name