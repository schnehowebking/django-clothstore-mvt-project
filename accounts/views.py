from django.shortcuts import get_object_or_404, render
from django.views.generic import *
from .forms import *
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from products.models import *
import logging
from django.contrib.sites.shortcuts import get_current_site

logger = logging.getLogger(__name__)


class UserRegistrationView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        current_site = get_current_site(self.request)
        domain = current_site.domain

        confirm_link = f"{self.request.scheme}://{domain}{reverse('activate', args=[uid, token])}"
        
        email_subject = "Confirm Your Email"
        email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        
        login(self.request, user)
        return super().form_valid(form)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    
    user.is_active = True
    user.save()
    logger.info(f"User {user.username} activated successfully.")
    return redirect('login')
 




class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'accounts/dashboard.html'
    model = User
    context_object_name = 'user_profile'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_wishlist_items = WishList.objects.filter(user=self.request.user).first()
        context['wishlist_items'] = user_wishlist_items.items.all() if user_wishlist_items else []

        user_purchase_items = Purchase.objects.filter(user=self.request.user)
        context['purchase_items'] = user_purchase_items

        return context

    

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        return reverse_lazy('dashboard')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Password changed successfully.')
            
            return redirect('dashboard')
    else:
        form = UserPasswordChangeForm(request.user)
    return render(request, './accounts/change_password.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


class UserAccountUpdateView(LoginRequiredMixin, View):
    template_name = 'accounts/dashboard.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user.customer)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form}) 
    
    

