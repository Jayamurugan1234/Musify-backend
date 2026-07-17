from django.db import models
from accounts.models import CustomUser
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

class Subscription(models.Model):

    PLAN_CHOICES = (

        ('free', 'Free'),

        ('premium', 'Premium'),
    )

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default='free'
    )

    active = models.BooleanField(default=True)

    start_date = models.DateTimeField(auto_now_add=True)

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )


    def activate_premium(self, days=30):

        self.plan = "premium"

        self.active = True

        self.start_date = timezone.now()

        self.end_date = timezone.now() + timedelta(days=days)

        self.save()

    def is_premium(self):

        return (
        self.plan == "premium"
        and self.active
        )


    def can_download(self):

        return self.is_premium()


    def can_access_early_releases(self):

        return self.is_premium()


    def can_use_hq_audio(self):

        return self.is_premium()


    def can_use_offline_mode(self):

        return self.is_premium()


    def can_use_ad_free(self):

        return self.is_premium()
    

    def can_use_ad_free(self):

        return self.is_premium()


    def __str__(self):

        return f"{self.user.username} - {self.plan}"
    

class Payment(models.Model):

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_id = models.CharField(
        max_length=255,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.status}"
    
    