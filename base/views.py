from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_protect
from .models import Expense, DailyIncome,Goal,Blog,Profile,Stock,FixedDeposit,LoanCalculation
from django.contrib.auth.models import User, auth
from django.shortcuts import HttpResponse
from decimal import Decimal
import json
from django.core.mail import send_mail
import csv
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from django.contrib import messages
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from django.core.exceptions import ValidationError
from datetime import timezone
from datetime import datetime
from django.db.models import F
from django.core.paginator import Paginator
import io
import base64
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def home(request):
    return render(request, 'base/home.html')

@login_required
def dashboard(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  
    
    expenses = Expense.objects.filter(user=user)
    total_income = DailyIncome.objects.filter(user=user).aggregate(Sum('income'))['income__sum'] or Decimal('0')
    total_expense = expenses.exclude(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    current_balance = total_income - total_expense
    if total_expense > total_income:
        subject = "⚠️ Warning: Your Expenses Exceed Your Income!"
        message = (
            f"Dear {user.username},\n\n"
            "We noticed that your total expenses have exceeded your total income.\n"
            f"📊 Total Income: ₹{total_income}\n"
            f"💸 Total Expense: ₹{total_expense}\n"
            "This might impact your financial stability. Please review your expenses and take necessary actions.\n\n"
            "Best regards,\n"
            "Smart Personal Finance Advisor"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        

    expense_data = expenses.exclude(type='INCOME').values('type').annotate(total=Sum('amount'))
    expense_labels = [expense['type'] for expense in expense_data]
    expense_data_values = [float(expense['total']) for expense in expense_data]

    daily_incomes = DailyIncome.objects.filter(user=user).values('date').annotate(total=Sum('income')).order_by('date')
    income_labels = [str(income['date']) for income in daily_incomes]
    income_data_values = [float(income['total']) for income in daily_incomes]

    context = {
        'user': user,
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'current_balance': float(current_balance),
        'expense_labels': json.dumps(expense_labels),
        'expense_data_values': json.dumps(expense_data_values),
        'income_labels': json.dumps(income_labels),
        'income_data_values': json.dumps(income_data_values),
        'profile': profile,  
        
    }
    return render(request, 'base/dashboard.html', context)


def log_in(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=username)
            check = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            check = authenticate(username=username, password=password)

        if check is not None:
            login(request, check)
            return redirect('dashboard')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'base/login.html')



@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cnfpassword = request.POST.get('confirm_password')
        dob_str = request.POST.get('dob')

        
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            #messages.info(request, 'Invalid Date of Birth format')
            return redirect('register')

        
        if dob >= date.today():
           # messages.info(request, 'Date of Birth must be in the past')
            return redirect('register')

        if password != cnfpassword:
           # messages.info(request, 'Password and Confirm password do not match')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            #messages.info(request, 'Email already registered')
            return redirect('register')

        if User.objects.filter(username=username).exists():
           # messages.info(request, 'Username already taken')
            return redirect('register')

        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=new_user, dob=dob)

       
        user_login = authenticate(username=username, password=password)
        if user_login is not None:
            login(request, user_login)
            return redirect('dashboard')

    return render(request, 'base/register.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def expense_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        expense_type = request.POST['type']
        amount = Decimal(request.POST['amount'])
        receipt = request.FILES.get('receipt') 
        Expense.objects.create(
            user=request.user,
            name=name,
            type=expense_type,
            amount=amount,
            receipt=receipt,
            created_at=now(),
            updated_at=now(),
        ).save()
        return redirect('dashboard')
    return render(request, 'base/add_expense.html')

@login_required
def expense_trac(request):
    user = request.user
    sort_by_expense = request.GET.get('sort_expense', 'created_at')
    order_expense = request.GET.get('order_expense', 'asc')
    sort_by_income = request.GET.get('sort_income', 'date')
    order_income = request.GET.get('order_income', 'asc')

    if order_expense == 'asc':
        expenses = Expense.objects.filter(user=user).order_by(F(sort_by_expense).asc())
    else:
        expenses = Expense.objects.filter(user=user).order_by(F(sort_by_expense).desc())

    if order_income == 'asc':
        incomes = DailyIncome.objects.filter(user=user).order_by(F(sort_by_income).asc())
    else:
        incomes = DailyIncome.objects.filter(user=user).order_by(F(sort_by_income).desc())

    #pagination for income 
    income_paginator = Paginator(incomes, 5)
    income_page_number = request.GET.get('income_page')
    income_page_obj = income_paginator.get_page(income_page_number)
    
    #paginator for expense
    expense_paginator = Paginator(expenses,5)
    expsene_page_numeber = request.GET.get('expense_page')
    expense_page_obj = expense_paginator.get_page(expsene_page_numeber)

    context ={
        'expense_page_obj': expense_page_obj,
        'income_page_obj': income_page_obj,    
        'expense_page_obj': expense_page_obj,
        'income_page_obj': income_page_obj,
        'sort_by_expense': sort_by_expense,
        'order_expense': order_expense,
        'sort_by_income': sort_by_income,
        'order_income': order_income,
    }
    
    return render(request, 'base/ExpenseTracking.html', context)

@login_required
def income_add(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        income_type = request.POST['income_type']
        today = now().date()

        daily_income, created = DailyIncome.objects.update_or_create(
            user=request.user,
            date=today,
            income_type=income_type,
            defaults={'income': amount}
        )

        if not created:
            daily_income.income = amount
            daily_income.save()
        
        return redirect('dashboard')
    return render(request, 'base/add_income.html')

# @login_required
@login_required
def expense_edit(request, pk):
    expense = Expense.objects.get(pk=pk)

    if request.method == 'POST':
        expense.name = request.POST.get('name')
        expense.type = request.POST.get('type')
        expense.amount = request.POST.get('amount')
        expense.receipt = request.FILES.get('receipt')
        expense.save()
        return redirect('dashboard')

    return render(request, 'base/edit_expense.html', {'expense': expense})

@login_required
def expense_delete(request,pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return render(request, 'base/delete_expense.html', {'expense': expense})

@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user, saved_already__lt=F('target_amount'))
    achieved_goals = Goal.objects.filter(user=request.user, saved_already__gte=F('target_amount'))
    for goal in goals:
        
        today = date.today()
        remaining_days = (goal.desired_date - today).days
        goal.remaining_days = remaining_days
    return render(request, 'base/goal_list.html', {'goals': goals, 'achieved_goals': achieved_goals})



def send_goal_completion_email(user, goal):
    """
    Send a congratulatory email when a goal is completed using SendGrid.
    """
    subject = "Congratulations! You've Achieved Your Financial Goal! 🎉"
    message = f"""
Dear {user.username},

Congratulations! You've successfully achieved your financial goal: "{goal.name}"!

Goal Details:
- Target Amount: ₹{goal.target_amount}
- Saved Amount:₹{goal.saved_already}
- Goal Description: {goal.note}

Keep up the great work with your financial planning!

Best regards,
Your Financial Tracker Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def goal_edit(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        previous_saved_amount = goal.saved_already
        goal.name = request.POST.get('name')
        goal.target_amount = Decimal(request.POST.get('target_amount'))
        goal.saved_already = Decimal(request.POST.get('saved_already'))
        
        
        desired_date_str = request.POST.get('desired_date')
        try:
           
            goal.desired_date = datetime.strptime(desired_date_str, '%Y-%m-%d').date()
            
            # Validate that the date is not in the past
            if goal.desired_date < date.today():
                messages.error(request, 'Goal date cannot be in the past')
                return render(request, 'base/goal_add.html', {'goal': goal})
                
        except ValueError:
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD')
            return render(request, 'base/goal_add.html', {'goal': goal})
        
        goal.note = request.POST.get('note')

        try:
            goal.clean()
            # Check if goal is newly completed
            if goal.saved_already >= goal.target_amount and previous_saved_amount < goal.target_amount:
                email_sent = send_goal_completion_email(request.user, goal)
                if email_sent:
                    messages.success(request, 'Congratulations! You have achieved your goal! We have sent you an email confirmation.')
                else:
                    messages.success(request, 'Congratulations! You have achieved your goal! (Email notification could not be sent)')
            
            goal.save()
            return redirect('goal_list')
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'base/goal_add.html', {'goal': goal})
    return render(request, 'base/goal_add.html', {'goal': goal})

def goal_add(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            target_amount = Decimal(request.POST.get('target_amount'))
            saved_already = Decimal(request.POST.get('saved_already'))
            
           
            desired_date_str = request.POST.get('desired_date')
            try:

                desired_date = datetime.strptime(desired_date_str, '%Y-%m-%d').date()
                
            
                if desired_date < date.today():
                    messages.error(request, 'Goal date cannot be in the past')
                    return render(request, 'base/goal_add.html')
                    
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD')
                return render(request, 'base/goal_add.html')
                
            note = request.POST.get('note')
           
            goal = Goal(
                user=request.user,
                name=name,
                target_amount=target_amount,
                saved_already=saved_already,
                desired_date=desired_date,
                note=note
            )
            
            goal.clean()
            goal.save()
            
            # Check if goal is completed upon creation
            if saved_already >= target_amount:
                email_sent = send_goal_completion_email(request.user, goal)
                if email_sent:
                    messages.success(request, 'Congratulations! You have achieved your goal! We have sent you an email confirmation.')
                else:
                    messages.success(request, 'Congratulations! You have achieved your goal! (Email notification could not be sent)')
            
            return redirect('goal_list')
            
        except (ValidationError, ValueError) as e:
            messages.error(request, str(e))
            return render(request, 'base/goal_add.html')
            
    return render(request, 'base/goal_add.html')

def blog_list(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 10)  
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'base/blog_list.html', {'page_obj': page_obj})
@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    # Calculate balance
    expenses = Expense.objects.filter(user=user)
    total_income = DailyIncome.objects.filter(user=user).aggregate(Sum('income'))['income__sum'] or Decimal('0')
    total_expense = expenses.exclude(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    current_balance = float(total_income - total_expense)  

    if request.method == 'POST':
        try:
            # Handle Gender change
            if 'gender' in request.POST:
                profile.gender = request.POST['gender']
                profile.save()
                
                # Return the new gender in the response
                return JsonResponse({
                    'success': True,
                    'message': 'Gender updated successfully!',
                    'gender': profile.gender,
                    'current_balance': current_balance
                })
            
            # Handle profile photo
            if 'profile_photo' in request.FILES:
                profile.profile_photo = request.FILES['profile_photo']
                profile.save()
                
                # Return the new image URL in the response
                return JsonResponse({
                    'success': True,
                    'message': 'Profile updated successfully!',
                    'photo_url': profile.profile_photo.url,
                    'current_balance': current_balance
                })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error updating profile: {str(e)}'
            })

    context = {
        'profile': profile,
        'current_balance': current_balance,
    }
    return render(request, 'base/profile.html', context)
@login_required
def download_income_report(request):
    """Generate a CSV for the authenticated user's income report within a given date range."""
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if not from_date or not to_date:
        return HttpResponse("Invalid date range.", status=400)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Income_Report_{from_date}_to_{to_date}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Income Type', 'Amount'])

    incomes = DailyIncome.objects.filter(user=request.user, date__range=[from_date, to_date])
    
    if not incomes.exists():
        writer.writerow(["No records found"])

    for income in incomes:
        writer.writerow([income.date, income.income_type, income.income])

    return response


@login_required
def download_expense_report(request):
    """Generate a CSV for the authenticated user's expense report within a given date range."""
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if not from_date or not to_date:
        return HttpResponse("Invalid date range.", status=400)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Expense_Report_{from_date}_to_{to_date}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Amount'])

    expenses = Expense.objects.filter(user=request.user, created_at__range=[from_date, to_date])

    if not expenses.exists():
        writer.writerow(["No records found"])

    for expense in expenses:
        writer.writerow([expense.created_at, expense.type, expense.amount])

    return response


@login_required
def download_comparative_report(request):
    """Generate a CSV comparing the authenticated user's income and expenses within a given date range."""
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if not from_date or not to_date:
        return HttpResponse("Invalid date range.", status=400)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Comparative_Report_{from_date}_to_{to_date}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Type', 'Category/Income Type', 'Amount'])

    expenses = Expense.objects.filter(user=request.user, created_at__range=[from_date, to_date])
    incomes = DailyIncome.objects.filter(user=request.user, date__range=[from_date, to_date])

    if not expenses.exists() and not incomes.exists():
        writer.writerow(["No records found"])
    
    for expense in expenses:
        writer.writerow([expense.created_at, 'Expense', expense.type, expense.amount])
    for income in incomes:
        writer.writerow([income.date, 'Income', income.income_type, income.income])

    return response





def send_test_email(request):
    try:
        send_mail(
            "Test Email",
            "Hello from Django!",
            "ridheshchauhan7@gmail.com",  # From email (must be verified in SendGrid)
            ["ridheshchauhan29@gmail.com"],  # Replace with recipient email
            fail_silently=False,
        )
        return JsonResponse({"message": "Email sent successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    



@login_required
def investment_dashboard(request):
    fixed_deposits = FixedDeposit.objects.filter(user=request.user)
    stocks = Stock.objects.filter(user=request.user)
    
    # Calculate total investments
    fd_total = fixed_deposits.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    stock_total = sum(stock.calculate_investment_value() for stock in stocks)
    
    context = {
        'fixed_deposits': fixed_deposits,
        'stocks': stocks,
        'fd_total': fd_total,
        'stock_total': stock_total,
        'total_investment': fd_total + stock_total
    }
    return render(request, 'base/invest_dash.html', context)

@login_required
def add_fixed_deposit(request):
    if request.method == 'POST':
        try:
            fd = FixedDeposit(
                user=request.user,
                bank_name=request.POST['bank_name'],
                amount=request.POST['amount'],
                interest_rate=request.POST['interest_rate'],
                start_date=request.POST['start_date'],
                maturity_date=request.POST['maturity_date'],
                receipt_number=request.POST['receipt_number']
            )
            fd.save()
            messages.success(request, 'Fixed Deposit added successfully!')
            return redirect('investment')
        except Exception as e:
            messages.error(request, f'Error adding Fixed Deposit: {str(e)}')
    return render(request, 'base/add_fd.html')
@login_required
def edit_fixed_deposit(request, pk):
    fd = get_object_or_404(FixedDeposit, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            fd.bank_name = request.POST['bank_name']
            fd.amount = request.POST['amount']
            fd.interest_rate = request.POST['interest_rate']
            fd.start_date = request.POST['start_date']
            fd.maturity_date = request.POST['maturity_date']
            fd.receipt_number = request.POST['receipt_number']
            fd.save()
            messages.success(request, 'Fixed Deposit updated successfully!')
            return redirect('investment')
        except Exception as e:
            messages.error(request, f'Error updating Fixed Deposit: {str(e)}')
    return render(request, 'base/edit_fd.html', {'fd': fd})
@login_required
def add_stock(request):
    if request.method == 'POST':
        try:
            stock = Stock(
                user=request.user,
                symbol=request.POST['symbol'],
                company_name=request.POST['company_name'],
                shares=request.POST['shares'],
                purchase_price=request.POST['purchase_price'],
                purchase_date=request.POST['purchase_date']
            )
            stock.save()
            messages.success(request, 'Stock added successfully!')
            return redirect('investment')
        except Exception as e:
            messages.error(request, f'Error adding Stock: {str(e)}')
    return render(request, 'base/add_stock.html')
@login_required
def edit_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            stock.symbol = request.POST['symbol']
            stock.company_name = request.POST['company_name']
            stock.shares = request.POST['shares']
            stock.purchase_price = request.POST['purchase_price']
            stock.purchase_date = request.POST['purchase_date']
            stock.save()
            messages.success(request, 'Stock updated successfully!')
            return redirect('investment')
        except Exception as e:
            messages.error(request, f'Error updating Stock: {str(e)}')
    return render(request, 'base/edit_stock.html', {'stock': stock})
@login_required
def delete_fixed_deposit(request, pk):
    fd = get_object_or_404(FixedDeposit, pk=pk, user=request.user)
    fd.delete()
    messages.success(request, 'Fixed Deposit deleted successfully!')
    return redirect('investment')
@login_required
def delete_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    stock.delete()
    messages.success(request, 'Stock deleted successfully!')
    return redirect('investment')
@login_required
def fixed_deposit_detail(request, pk):
    fd = get_object_or_404(FixedDeposit, pk=pk, user=request.user)
    maturity_amount = fd.calculate_maturity_amount()
    context = {
        'fd': fd,
        'maturity_amount': maturity_amount
    }
    return render(request, 'base/fd_detail.html', context)
@login_required
def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    investment_value = stock.calculate_investment_value()
    context = {
        'stock': stock,
        'investment_value': investment_value
    }
    return render(request, 'base/stock_detail.html', context)

def calculate_emi(request):
    if request.method == 'POST':
        loan_amount = float(request.POST.get('loan_amount', 0))
        interest_rate = float(request.POST.get('interest_rate', 0))
        loan_tenure = int(request.POST.get('loan_tenure', 0))
        
        # Monthly interest rate
        monthly_rate = (interest_rate / 12) / 100
        
        # Calculate EMI using formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
        if monthly_rate > 0:
            emi = loan_amount * monthly_rate * (pow(1 + monthly_rate, loan_tenure)) / (pow(1 + monthly_rate, loan_tenure) - 1)
        else:
            emi = loan_amount / loan_tenure
            
        total_interest = (emi * loan_tenure) - loan_amount
        
        # Save calculation
        LoanCalculation.objects.create(
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            loan_tenure=loan_tenure,
            monthly_emi=emi,
            total_interest=total_interest
        )
        
        return JsonResponse({
            'emi': round(emi, 2),
            'total_interest': round(total_interest, 2)
        })
    
    return render(request, 'base/calculator.html')