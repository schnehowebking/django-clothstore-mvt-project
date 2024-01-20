from django.shortcuts import redirect, render
from django.contrib import messages
from products.models import *
from .models import *

# Create your views here.

def home(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        products = Product.objects.filter(category = category)
    for product in products:
        product.avg_rating = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    return render(request, 'index.html', {'products':products, 'categories':categories})
    
def contact(request):

    return render(request, 'contact.html')


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactUs.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Your Contacts Has been Submitted')
        return redirect('contact')

    return render(request, 'contact.html')