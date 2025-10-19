from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['id', 'slug']), models.Index(fields=['name']), models.Index(fields=['-created'])]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.slug])
    
    def sell_price(self):
        if self.discount:
            return round(self.price-self.price*self.discount/100,2)
        return self.price
    
