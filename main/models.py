from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Min
from django.db.models.signals import post_save
from django.dispatch import receiver

class Restaurant(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    address = models.CharField(max_length=300, verbose_name="Адрес")
    latitude = models.FloatField(blank=True, null=True, verbose_name="Широта")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Долгота")
    photo = models.ImageField(upload_to='restaurants/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.name

    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else None

    def min_price(self):
        min_price = self.dishes.aggregate(Min('price'))['price__min']
        return min_price if min_price else None

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes', verbose_name="Ресторан")
    name = models.CharField(max_length=200, verbose_name="Название блюда")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    photo = models.ImageField(upload_to='dishes/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews', verbose_name="Ресторан")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} - {self.rating}★"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class Tour(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название тура")
    description = models.TextField(verbose_name="Описание")
    location = models.CharField(max_length=200, verbose_name="Локация", help_text="Например: Центральный район, Красноярск")
    duration = models.CharField(max_length=100, verbose_name="Продолжительность", blank=True, help_text="Например: 2 дня / 1 ночь")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    photo = models.ImageField(upload_to='tours/', blank=True, null=True, verbose_name="Главное фото")
    restaurants = models.ManyToManyField(Restaurant, related_name='tours', verbose_name="Включённые рестораны")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        avg = self.tour_reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else None

    def review_count(self):
        return self.tour_reviews.count()

    class Meta:
        verbose_name = "Гастротур"
        verbose_name_plural = "Гастротуры"

class TourReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tour_reviews', verbose_name="Тур")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.name} - {self.rating}★"

    class Meta:
        verbose_name = "Отзыв на тур"
        verbose_name_plural = "Отзывы на туры"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")

    def __str__(self):
        return f"{self.user.username} - {self.phone}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings', verbose_name="Тур")
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")  # добавлено поле email
    date = models.DateField(verbose_name="Желаемая дата")
    guests = models.PositiveIntegerField(default=1, verbose_name="Количество гостей")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")

    def __str__(self):
        return f"{self.name} - {self.tour.name} ({self.date})"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)