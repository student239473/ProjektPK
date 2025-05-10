from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from .models import Car
from .forms import CarForm, RegisterForm
from datetime import datetime
from django.http import HttpResponse


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def confirmation(request):
    return render(request, 'main/confirmation.html')


def is_admin(user):
    return user.is_superuser


@login_required
def cars(request):
    if request.method == 'POST' and request.user.is_staff:
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Car added successfully!")
            return redirect('cars')
    else:
        form = CarForm()

    cars = Car.objects.all()

    if request.user.is_staff:
        return render(request, 'main/cars.html', {'cars': cars, 'form': form})
    else:
        return render(request, 'main/cars.html', {'cars': cars})


def reservation(request):
    if request.method == 'POST':
        rental_date_str = request.POST.get('rental_date')
        return_date_str = request.POST.get('return_date')
        car_choice = request.POST.get('car_choice')

        rental_date = datetime.strptime(rental_date_str, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()

        if return_date <= rental_date:
            return HttpResponse("Data zwrotu musi być późniejsza niż data wynajmu.", status=400)

        car_prices = {
            'BMW X5': 300,
            'Audi A4': 250,
            'Mercedes C-Class': 280,
            'Volkswagen Golf': 220,
            'Toyota Corolla': 200,
            'Ford Focus': 210
        }

        rental_duration = (return_date - rental_date).days
        car_price_per_day = car_prices.get(car_choice, 0)
        total_price = car_price_per_day * rental_duration

        return render(request, 'main/confirmation.html', {
            'rental_date': rental_date_str,
            'return_date': return_date_str,
            'car_choice': car_choice,
            'total_price': total_price,
        })
    else:
        return render(request, 'main/reservation.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if request.session.get('next'):
                return redirect(request.session.pop('next'))
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_user')

    if request.GET.get('next'):
        request.session['next'] = request.GET['next']

    return render(request, 'main/users/login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])

            # If user checks 'is_admin', grant admin rights
            if form.cleaned_data['is_admin']:
                user.is_staff = True  # Grant admin privileges

            user.save()

            # Log in the user
            login(request, user)
            return redirect('index')
        else:
            # Displaying specific form errors
            messages.error(request, 'Formularz jest nieprawidłowy.')
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'main/users/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required
@user_passes_test(is_admin)
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    messages.success(request, 'Car deleted successfully!')
    return redirect('cars')