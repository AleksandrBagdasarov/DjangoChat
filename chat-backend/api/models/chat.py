from django.db import models


class Chat(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "chat"
        verbose_name = "chat"
        verbose_name_plural = "chat"
