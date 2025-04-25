from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def cars(request):
    return render(request, 'main/cars.html')

def confirmation(request):
    return render(request, 'main/confirmation.html')



from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

def reservation(request):
    if request.method == 'POST':
        rental_date_str = request.POST.get('rental_date')
        return_date_str = request.POST.get('return_date')
        car_choice = request.POST.get('car_choice')

        # Przekształcanie dat na obiekty datetime
        rental_date = datetime.strptime(rental_date_str, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()

        # Sprawdzamy, czy data zwrotu jest późniejsza niż data wynajmu
        if return_date <= rental_date:
            return HttpResponse("Data zwrotu musi być późniejsza niż data wynajmu.", status=400)

        # Ceny samochodów
        car_prices = {
            'BMW X5': 300,
            'Audi A4': 250,
            'Mercedes C-Class': 280,
            'Volkswagen Golf': 220,
            'Toyota Corolla': 200,
            'Ford Focus': 210
        }

        # Obliczanie liczby dni wynajmu
        rental_duration = (return_date - rental_date).days
        car_price_per_day = car_prices.get(car_choice, 0)
        total_price = car_price_per_day * rental_duration

        # Przekierowanie na stronę potwierdzenia rezerwacji
        return render(request, 'main/confirmation.html', {
            'rental_date': rental_date_str,
            'return_date': return_date_str,
            'car_choice': car_choice,
            'total_price': total_price,
        })
    else:
        return render(request, 'main/reservation.html')
    