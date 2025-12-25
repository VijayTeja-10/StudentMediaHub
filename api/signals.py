from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Material

@receiver(signal=post_delete,sender=Material)
def post_material_delete(sender,instance,**kwargs):
    if instance.material: instance.material.delete(save=False)