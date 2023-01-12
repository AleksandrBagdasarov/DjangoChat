from django.db import models


class ScheduledMessage(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, null=False)
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

    execute_at = models.DateTimeField(null=False)
    executed = models.BooleanField(default=False)

    class Meta:
        db_table = "scheduled_message"
        verbose_name = "scheduled_message"
        verbose_name_plural = "scheduled_message"
        indexes = [
            models.Index(
                fields=[
                    "execute_at",
                ]
            ),
            models.Index(
                fields=[
                    "executed",
                ]
            ),
        ]
