from django.shortcuts import render, redirect
from .models import CarouselSlide
def home(request):
    carousel = CarouselSlide.objects.filter(is_active=True)
    return render(request, 'home.html', {'carousel': carousel})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def classes(request):
    return render(request, 'classes.html')

def campus(request):
    return render(request, 'campus.html')

def classes(request):
    return render(request, 'classes.html')

def primary(request):
    return render(request, 'primary.html')

def nursery(request):
    return render(request, 'nursery.html')

def main(request):
    return render(request, 'main.html')

def annex(request):
    return render(request, 'annex.html')

def golden(request):
    return render(request, 'golden.html')

def muni(request):
    return render(request, 'muni.html')

def admissions(request):
    return render(request, 'admissions.html')

def news(request):
 
    context = {
        'title': 'News & Events',
        #'news_items': NewsItem.objects.all() 
    }
    return render(request, 'news.html', context)

# views.py
from django.shortcuts import render
from .models import GalleryImage  # You'll need to create this model

def gallery(request):
    categories = GalleryImage.objects.values_list('category', flat=True).distinct()
    images = GalleryImage.objects.all().order_by('-upload_date')
    
    # Optional: Group by category if you want tabs/filtering
    images_by_category = {}
    for category in categories:
        images_by_category[category] = GalleryImage.objects.filter(category=category)
    
    context = {
        'categories': categories,
        'images': images,
        'images_by_category': images_by_category,
    }
    return render(request, 'gallery.html', context)


def gallery_image_detail(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    return render(request, 'gallery/detail.html', {'image': image})



def privacy(request):
    return render(request, 'privacy.html')  

def terms(request):
    return render(request, 'terms.html')  
def sitemap(request):
    return render(request, 'sitemap.html')

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import News, Subscriber
from .forms import SubscriberForm
from django.contrib import messages
from django.http import JsonResponse

class NewsListView(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 5
    
    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-published_date')

class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    
    def get_queryset(self):
        return News.objects.filter(is_published=True)


def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            
            try:
                # Send welcome email
                send_mail(
                    'Thanks for subscribing to Oasis Schools Arua News',
                    f"Hello {subscriber.name},\n\nThank you for subscribing to our newsletter. "
                    f"You'll now receive updates about our latest news and events.\n\n"
                    f"Best regards,\nOasis Schools Arua Team",
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    fail_silently=False,
                )
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'You have successfully subscribed to our newsletter!'
                    })
                
                messages.success(request, 'You have successfully subscribed to our newsletter!')
                return redirect('news_list')
                
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Subscription received but email failed to send.'
                    }, status=500)
                
                messages.warning(request, 'Subscription received but email failed to send.')
                return redirect('news_list')
        
        # Form is invalid
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data(),
                'message': 'Please correct the errors below.'
            }, status=400)
        
        # For regular form submission with errors
        return render(request, 'news/subscribe.html', {'form': form})
    
    # GET request - show empty form
    form = SubscriberForm()
    return render(request, 'subscribe.html', {'form': form})

# Admin function to send notifications (add to admin.py or create a management command)
def send_news_notification(news):
    subscribers = Subscriber.objects.filter(is_active=True)
    for subscriber in subscribers:
        send_mail(
            f'New Update from Oasis Schools Arua: {news.title}',
            f"Hello {subscriber.name},\n\n"
            f"We have a new update for you:\n\n"
            f"{news.title}\n\n"
            f"{news.content[:200]}...\n\n"
            f"Read more: https://yourdomain.com{news.get_absolute_url()}\n\n"
            f"Best regards,\nOasis Schools Arua Team",
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.email],
            fail_silently=False,
        )