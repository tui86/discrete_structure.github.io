from django.db import models

# Create your models here.
class RelationModel(models.Model):
    name = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}: {self.count}"