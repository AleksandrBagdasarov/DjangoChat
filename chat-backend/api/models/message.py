from django.db import models


class Message(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, null=False)
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        db_table = "message"
        verbose_name = "message"
        verbose_name_plural = "message"
        indexes = [
            models.Index(
                fields=[
                    "chat",
                ]
            ),
            models.Index(
                fields=[
                    "user",
                ]
            ),
            models.Index(
                fields=[
                    "created_at",
                ]
            ),
        ]
