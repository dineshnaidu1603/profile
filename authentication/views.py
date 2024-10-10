from django.shortcuts import render, redirect
from .models import Member
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password


# Registration View
def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        
        hashed_password = make_password(password)  # Hash the password
        member = Member(full_name=full_name, email=email, password=hashed_password)
        member.save()
        return redirect('login')
    return render(request, 'register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            member = Member.objects.get(email=email)
            if check_password(password, member.password):
                # Log in the user
                request.session['member_id'] = member.id
                request.session['member_email'] = member.email
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except Member.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# Dashboard View
def dashboard(request):
    # Check if the user is logged in by looking for session data
    if 'member_id' not in request.session:
        return redirect('login')
    member_id = request.session['member_id']
    member = Member.objects.get(id=member_id)
    return render(request, 'dashboard.html', {'user': member})

# Profile View
def profile(request):
    # Check if the user is logged in by looking for session data
    if 'member_id' not in request.session:
        return redirect('login')

    member_id = request.session['member_id']
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        return redirect('register')  # If no member found, redirect to registration page

    if request.method == 'POST':
        
        member.full_name = request.POST['full_name']
        member.age = request.POST.get('age', '')
        member.location = request.POST.get('location', '')
        member.save()
        return redirect('dashboard')  # Redirect to dashboard after updating profile

    return render(request, 'profile.html', {'member': member})
