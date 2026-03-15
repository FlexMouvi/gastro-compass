from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Restaurant, Dish, Review, Tour, TourReview, Booking
from .forms import (
    ReviewForm, TourReviewForm,
    CustomUserCreationForm, CustomAuthenticationForm,
    BookingForm
)

def send_booking_notification(booking):
    """
    Отправляет уведомление администратору о новом бронировании.
    """
    subject = f'Новое бронирование: {booking.tour.name}'
    message = f'''
    Новое бронирование тура!

    Тур: {booking.tour.name}
    Имя: {booking.name}
    Телефон: {booking.phone}
    Желаемая дата: {booking.date}
    Количество гостей: {booking.guests}
    Комментарий: {booking.comment}

    Дата заявки: {booking.created_at.strftime('%d.%m.%Y %H:%M')}
    '''
    admin_email = 'admin@example.com'  # замените на свой email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL or 'noreply@example.com',
        [admin_email],
        fail_silently=False,
    )

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tour_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tour_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('tour_list')

def tour_list(request):
    tours = Tour.objects.all()
    user_name = request.user.get_full_name() or request.user.username if request.user.is_authenticated else ''
    user_phone = request.user.profile.phone if request.user.is_authenticated else ''
    context = {
        'tours': tours,
        'booking_form': BookingForm(),
        'user_name': user_name,
        'user_phone': user_phone,
    }
    return render(request, 'main/tour_list.html', context)

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    reviews = tour.tour_reviews.all().order_by('-created_at')
    user_name = request.user.get_full_name() or request.user.username if request.user.is_authenticated else ''
    user_phone = request.user.profile.phone if request.user.is_authenticated else ''
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = TourReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            return redirect('tour_detail', pk=tour.pk)
    else:
        form = TourReviewForm()
    context = {
        'tour': tour,
        'reviews': reviews,
        'form': form,
        'booking_form': BookingForm(),
        'user_name': user_name,
        'user_phone': user_phone,
    }
    return render(request, 'main/tour_detail.html', context)

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    user_name = request.user.get_full_name() or request.user.username if request.user.is_authenticated else ''
    user_phone = request.user.profile.phone if request.user.is_authenticated else ''
    context = {
        'restaurants': restaurants,
        'booking_form': BookingForm(),
        'user_name': user_name,
        'user_phone': user_phone,
    }
    return render(request, 'main/restaurant_list.html', context)

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    dishes = restaurant.dishes.all()
    reviews = restaurant.reviews.all().order_by('-created_at')
    user_name = request.user.get_full_name() or request.user.username if request.user.is_authenticated else ''
    user_phone = request.user.profile.phone if request.user.is_authenticated else ''
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.save()
            return redirect('restaurant_detail', pk=restaurant.pk)
    else:
        form = ReviewForm()
    context = {
        'restaurant': restaurant,
        'dishes': dishes,
        'reviews': reviews,
        'form': form,
        'booking_form': BookingForm(),
        'user_name': user_name,
        'user_phone': user_phone,
    }
    return render(request, 'main/restaurant_detail.html', context)

def booking_view(request):
    if request.method == 'POST':
        tour_id = request.POST.get('tour_id')
        tour = get_object_or_404(Tour, pk=tour_id)
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            send_booking_notification(booking)  # <-- вызов функции
            messages.success(request, 'Спасибо! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.')
        else:
            messages.error(request, 'Ошибка в форме. Проверьте данные.')
        return redirect(request.META.get('HTTP_REFERER', 'tour_list'))
    return redirect('tour_list')