from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from robots.models import Robot
from orders.models import Order


@receiver(post_save, sender=Robot)
def send_robot_available_notification(sender, instance, **kwargs):
    print("TRY SEND EMAIL")
    orders = Order.objects.filter(model=instance.model, version=instance.version, fulfilled=False)
    for order in orders:
        send_mail(
            'Робот доступен',
            f'Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model},'
            f'версии {instance.version}.\n'
            f'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами',
            [order.customer.email],
            fail_silently=False
        )
        order.fulfilled = True
        order.save()
