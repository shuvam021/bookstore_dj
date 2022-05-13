from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from api.middleware import get_current_user


# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.pk}"


class User(BaseModel, AbstractUser):
    class Meta(BaseModel.Meta):
        db_table = 'user'

    phone = models.CharField(max_length=12)


@receiver(pre_save, sender=User)
def encrypt_password(sender, instance, *args, **kwargs):
    if not instance.is_superuser and instance.password is not None:
        instance.set_password(instance.password)
    return instance


class Book(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'book'

    author = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=100)


class Order(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'order'

    total_price = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=get_current_user)
    status = models.IntegerField()
    books = models.ManyToManyField("Book")


class Cart(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'cart'

    total_quantity = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=5)
    status = models.IntegerField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=get_current_user)
    product = models.ManyToManyField('Book')
