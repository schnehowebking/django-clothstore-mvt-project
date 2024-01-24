from django.db.models import Count, Avg, ExpressionWrapper, F, fields
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets, filters, pagination

from cart.models import Cart
from .models import Product, Review, WishList
from categories.models import *
from .forms import *
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def shop(request, category_slug=None, size_slug=None, color_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category)
    if size_slug is not None:
        size = Size.objects.get(slug=size_slug)
        products = Product.objects.filter(size=size)
    if color_slug is not None:
        color = Color.objects.get(slug=color_slug)
        products = Product.objects.filter(color=color)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price is not None:
        products = products.filter(price__gte=min_price)

    if max_price is not None:
        products = products.filter(price__lte=max_price)

    
    sort_by_price = request.GET.get('sort_by_price', 'asc')


   



    if sort_by_price == 'asc':
        products = products.order_by('price')
    elif sort_by_price == 'desc':
        products = products.order_by('-price')

    for product in products:
        product.popularity = ExpressionWrapper(
            F('purchase_set__count') + Avg('reviews__rating'),
            output_field=fields.FloatField()
        )
        product.avg_rating = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    

         # Configure pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

  

    return render(request, './products/shop.html', {'products': products, 'categories': categories, 'sizes':sizes, 'colors':colors})


class ProductDetailsPageView(DetailView):
    model = Product
    template_name = './products/product_details.html'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        if self.request.user.is_authenticated:
            user_has_bought_product = Purchase.objects.filter(user=self.request.user, product=product).first()
            can_add_review = user_has_bought_product.user_id == self.request.user.id if user_has_bought_product else False
        else:
            user_has_bought_product = None
            can_add_review = False

        reviews = Review.objects.filter(product=product)
        average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

        review_form = ReviewForm

        context['reviews'] = reviews
        context['can_add_review'] = can_add_review
        context['review_form'] = review_form
        context['average_rating'] = average_rating

        return context

   
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.product = product
            review.save()
            messages.success(request, 'Review added successfully.')
            return redirect('productDetailspage', product_id=product_id)
        else:
            messages.error(request, 'Error adding review. Please check your input.')
            return redirect('productDetailspage', product_id=product_id)

    return redirect('productDetailspage', product_id=product_id)




@method_decorator(login_required, name='dispatch')
class BuyProductView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user=request.user
        purchase_price = product.price
        if user.customer.balance < purchase_price:
            messages.error(request, "Don's have enough balance for puschase")
            return redirect('product_detail', product_id=product_id)


        if product.quantity <= 0:
            messages.error(request, "Product out of stock.")
            return redirect('product_detail', product_id=product_id)


        purchase_entry = Purchase.objects.create(
            user=user,
            product=product,
            purchase_date=timezone.now(),
            purchase_price=purchase_price,
        )

        product.quantity -= 1
        product.save()
        user.customer.balance -= purchase_price
        user.customer.save()

        messages.success(request, "Product purchased successfully.")
        return redirect('dashboard')
    
@method_decorator(login_required, name='dispatch')
class BuyCartProductView(View):
    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = cart.cartitem_set.all()

        total_price = sum(cart_item.product.price for cart_item in cart_items)

        if user.customer.balance < total_price:
            messages.error(request, "You don't have enough balance to purchase all items in the cart.")
            return redirect('dashboard')

        for cart_item in cart_items:
            product = cart_item.product
            purchase_price = product.price

            purchase_entry = Purchase.objects.create(
                user=user,
                product=product,
                purchase_date=timezone.now(),
                purchase_price=purchase_price,
            )


            product.quantity -= 1
            product.save()
            user.customer.balance -= total_price
            user.customer.save()
            cart_item.delete()

        messages.success(request, "All items from the cart have been purchased successfully.")
        return redirect('dashboard')
    

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    wish_list, created = WishList.objects.get_or_create(user=user)

    if request.method == 'POST':
        print(product_id)
        wish_list.items.add(product)
        messages.success(request, "Product Wishlisted successfully.")
        return redirect('dashboard')
    return render(request, 'products/product_details.html', {'product': product})



