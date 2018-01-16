from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    CLG_CHOICES = (
        ('MIT', 'Mahakal Institute Of Technology'),
        ('MITM', 'Mahakal Institute Of Technology And Management'),
    )
    BRANCH_CHOICES = (
        ('CS', 'Computer Science And Engineering'),
        ('IT', 'Information Technology'),
        ('CE', 'Civil Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('EC', 'Electronic Engineering'),
    )
    college = models.CharField(max_length=5,choices=CLG_CHOICES)
    branch = models.CharField(max_length=5,choices=BRANCH_CHOICES)
    birth_date = models.DateField(blank=True, null=True,help_text='YYYY-MM-DD')
    phone = models.CharField(max_length=10)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return "profile of {}".format(self.user)



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,db_index=True,unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET('None'), related_name='products')
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created','name'] #('name','-created',)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id, self.slug])

class Slide(models.Model):
    image_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200,db_index=True)
    image = models.ImageField(upload_to='slider/%Y/%m/%d',blank=False)
    description = models.TextField(blank=True,null=True)
    slide = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)