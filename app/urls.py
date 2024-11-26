from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . forms import *

urlpatterns = [
    path('',views.ProductView.as_view()),
    path('product-detail/<int:pk>', views.product_details_view.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('plus_cart/', views.plus_cart),
    path('minus_cart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.Customerprofile.as_view(), name='profile'),
    path('address/', views.Address.as_view(), name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=Changepassword), name='changepassword'),
    path('passchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/changepassworddone.html'), name='password_change_done'),

    path('reset-pass/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=passwordresetform), name='password_reset'),
    path('reset-pass/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),    
    path('resetpass-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=passwordSetForm), name='password_reset_confirm'),
    path('reset-pass-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),


    path('mobile/', views.mobile_view.as_view(), name='mobile'),
    path('mobiledata/<slug:data>', views.mobile_view.as_view(), name='mobiledata'),
    path('laptop/', views.laptop_view.as_view(), name='laptop'),
    path('laptopdata/<slug:data>', views.laptop_view.as_view(), name='laptopdata'),
    path('topwear/', views.topwear_view.as_view(), name='topwear'),
    path('topweardata/<slug:data>', views.topwear_view.as_view(), name='topweardata'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name = 'app/login.html',authentication_form = LoginForm),name='login'),
    path('logout/',views.custom_logout_view.as_view(), name='logout'),
    path('registration/', views.customerregistration.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
