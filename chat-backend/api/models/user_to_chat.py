from django.db import models


class UserToChat(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_to_chat"
        verbose_name = "user_to_chat"
        verbose_name_plural = "user_to_chat"
