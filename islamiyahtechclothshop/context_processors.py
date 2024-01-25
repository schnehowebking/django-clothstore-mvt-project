from cart.models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated and request.user.is_active:
        count = CartItem.objects.filter(cart__user=request.user).count()
        return {"cart_item_count": count}
    return {}