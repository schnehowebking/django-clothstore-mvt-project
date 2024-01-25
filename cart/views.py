from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages


# Create your views here.
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product added to cart successfully.")
    return redirect('view_cart')



@login_required
def view_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.cartitem_set.all()
    total_subtotal = sum(item.get_subtotal() for item in cart_items)

    #NEED TO PASS SUBTOTAL

    print(cart_items)

    return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'cart': cart, 'total_subtotal': total_subtotal})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    messages.success(request, "Product removed from cart successfully.")
    return redirect('view_cart')


@login_required
def clear_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart.cartitem_set.all().delete()
    messages.success(request, "Cart cleared successfully.")
    return redirect('view_cart')