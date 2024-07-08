from django.db import models

class Todo(models.Model):
    todo = models.TextField()

    def __str__(self):
        return self.todo[:50]