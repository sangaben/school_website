from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name_plural = "News"
        ordering = ['-published_date']

class CarouselSlide(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='carousel/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    


# models.py
from django.db import models
from django.utils import timezone

class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('events', 'School Events'),
        ('sports', 'Sports'),
        ('academics', 'Academics'),
        ('arts', 'Arts & Culture'),
        ('facilities', 'School Facilities'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']