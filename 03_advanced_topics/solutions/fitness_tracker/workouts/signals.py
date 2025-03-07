from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Workout
from django.core.mail import send_mail

@receiver(post_save, sender=Workout)
def notify_admin_on_workout(sender, instance, created, **kwargs):
    if created and instance.user.role == 'admin':
        send_mail(
            'Новая тренировка добавлена!',
            f'Пользователь {instance.user.username} создал тренировку: {instance.name}',
            'from@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )