from django.urls import path, include
from . import views

from Store.controller import authview ,order

urlpatterns = [
     
  
         
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("category/<slug:slug>/", views.categoryview, name="categoryview"),
    path("product/<slug:pslug>/<slug:vslug>/", views.productview, name="productview"),
    path("settings/", views.settingsview, name='settingsview'),
    
    path("cart/", views.cart, name='cart_page'),
    path('cart_count_increment/<uuid:id>/', views.cart_count_increase, name="cart_count_increment"),
    path('cart_count_decrement/<uuid:id>/', views.cart_count_decrease, name="cart_count_decrement"),
    path("add_to_cart/<slug:slug>/", views.add_to_cart, name='add_to_cart'),
    path("add_to_cart_button/<slug:slug>/", views.add_to_cart_button, name='add_to_cart_button'),
    path("remove_from_cart/<slug:slug>/", views.remove_from_cart, name='remove_from_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('add_address/', views.add_address, name='add_address'),
    path('edit_address/<uuid:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<uuid:address_id>/', views.delete_address, name='delete_address'),
   
    
    
    path('place-order/', views.placeorder, name='placeorder'),
    path('my-orders/', order.index, name="myorders"),
    path('view-order/<str:t_no>', order.orderview, name='orderview'),
    path('delete_order/<str:pk>', order.delete_order, name="delete_order"),
    path('download/<str:id>', order.UserInvoice.as_view(), name="download"),

    
    # path('paypal/', include('paypal.standard.ipn.urls')),
    
      
    path('promocode_view/', views.promocode_view, name='promocode_view'),
   
    path('register/', authview.Register.as_view(), name="register"),
    path('verify/<str:key>/',authview.VerifyOtpView.as_view(),name='otp'),
    path('resend_otp/<str:key>/', authview.ResendOTP.as_view(), name='resend_otp'),
    path('forgot_password/', authview.ForgotPassword.as_view(), name='forgot'),
    path('rreset_password/<str:encrypt_id>/',authview.UserResetPassword.as_view(),name='reset'),
    path('login/',authview.SignIn.as_view(), name="loginpage"),
    path('logout/', authview.Logoutpage.as_view(), name="logout"),
    
    path('edit_profile/',views.edit_profile, name="edit_profile"),
    
    
    
    path('profile_view/',views.profile_view, name="profile_view"),
    path('profile_order/',views.profile_order, name="profile_order"),
    path('profile_address/',views.profile_address, name="profile_address"),
    
    
    path('charge/', views.charge, name="charge"),
    
]

