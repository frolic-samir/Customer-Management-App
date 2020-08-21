from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer


@receiver(post_save, sender=User)
def createCustomerProfile(sender, created, instance, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(user=instance, name=instance)

# post_save.connect(createCustomerProfile,sender=User)
