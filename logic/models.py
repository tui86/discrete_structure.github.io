from django.db import models

class LogicModel(models.Model):
    name = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}: {self.count}"
# Create your models here.
