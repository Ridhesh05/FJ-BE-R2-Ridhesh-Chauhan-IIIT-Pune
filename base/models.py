from django.db import models
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal

User = get_user_model()

class Expense(models.Model):
    EXPENSE_TYPES = [
        ('FOOD', 'Food'),
        ('TRAVEL', 'Travel'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('MEDICAL', 'Medical'),
        ('EDUCATION', 'Education'),
        ('HOUSING', 'Housing'),
        ('SHOPPING', 'Shopping'),
        ('VEHICLE', 'Vehicle'),
        ('INVESTMENT', 'Investment'),
        ('DUES', 'Dues'),  
        ('LENDING', 'Lending'),   
        ('GIFT', 'Gifts'),  
        ('GAMBLING', 'Gambling'),    
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=320, choices=EXPENSE_TYPES)
    date = models.DateField(default=date.today, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DailyIncome(models.Model):
    INCOME_TYPES = [
        ('CHEQUES', 'Cheques'),
        ('GRANTS', 'Grants'),
        ('INTEREST', 'Interest'),
        ('DIVIDENDS', 'Dividends'),
        ('GAMBLING', 'Gambling'),
        ('REFUNDS', 'Refunds (Tax)'),
        ('RENTAL', 'Rental Income'),
        ('SALE', 'Sale'),
        ('WAGES', 'Wages'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    income_type = models.CharField(max_length=50, choices=INCOME_TYPES)
    income = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'date', 'income_type')

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.income_type} - ${self.income}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Notification.objects.create(
            user=self.user,
            message=f"New income added: ${self.income}",
            link="/income/list/"  # Update with actual URL
        )


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    saved_already = models.DecimalField(max_digits=10, decimal_places=2)
    desired_date = models.DateField()
    note = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.desired_date}"

    def clean(self):
        if self.desired_date < timezone.now().date():
            raise ValidationError("The desired date cannot be in the past.")

    @property
    def progress_percentage(self):
        return int((self.saved_already / self.target_amount) * 100) if self.target_amount > 0 else 0

    @property
    def days_remaining(self):
        return (self.desired_date - timezone.now().date()).days

    def save(self, *args, **kwargs):
        # Check if goal was previously not achieved but is now achieved
        goal_previously = None
        if self.pk:  # If the goal already exists (not a new goal)
            goal_previously = Goal.objects.get(pk=self.pk)

        super().save(*args, **kwargs)  # Save the updated goal first

        # If goal_previously exists and it was not achieved before but now it is achieved, send an email
        if goal_previously and goal_previously.saved_already < goal_previously.target_amount and self.saved_already >= self.target_amount:
            send_mail(
                subject="🎉 Goal Achieved!",
                message=f"Dear {self.user.username},\n\nCongratulations! You have successfully achieved your goal: {self.name}. Keep saving and achieving more!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.user.email],
                fail_silently=False,
            )



class Blog(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class Profile(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        max_length=255,
        null=True,
        blank=True,
        default='profile_photos/default_profile.jpg'
    )
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Delete old file when replacing with new file
        try:
            old_instance = Profile.objects.get(id=self.id)
            if old_instance.profile_photo != self.profile_photo:
                old_instance.profile_photo.delete(save=False)
        except Profile.DoesNotExist:
            pass
        super().save(*args, **kwargs)

class FixedDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    maturity_date = models.DateField()
    receipt_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_maturity_amount(self):
        duration = (self.maturity_date - self.start_date).days / 365.25
        maturity_amount = float(self.amount) * (1 + float(self.interest_rate)/100) ** duration
        return round(Decimal(maturity_amount), 2)

    def __str__(self):
        return f"{self.bank_name} - {self.receipt_number}"
class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100)
    shares = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_investment_value(self):
        return self.shares * self.purchase_price

    def __str__(self):
        return f"{self.symbol} - {self.shares} shares"
class LoanCalculation(models.Model):
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_tenure = models.IntegerField()
    monthly_emi = models.DecimalField(max_digits=10, decimal_places=2)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan Calculation - {self.created_at}"        