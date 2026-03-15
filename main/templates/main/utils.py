from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

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