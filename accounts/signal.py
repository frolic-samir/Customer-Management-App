from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer


@receiver(post_save, sender=User)
def createCustomerProfile(sender, created, instance, **kwargs):
    group_exist = Group.objects.exists()
    if not group_exist:
        Group.objects.create(name='admin')
        Group.objects.create(name='customer')

    if created and not instance.is_staff:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(user=instance, name=instance)
    elif created and instance.is_staff:
        group = Group.objects.get(name='admin')
        instance.groups.add(group)

# post_save.connect(createCustomerProfile,sender=User)
