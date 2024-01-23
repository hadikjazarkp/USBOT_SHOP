from django.urls import path
from . import views



urlpatterns=[
    
    
    path('wishlist/', views.WishlistView.as_view(), name='wishlist_view'),
    path('add_to_wishlist/<slug:slug>/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path("add_to_wishlist_button/<slug:slug>/", views.add_to_wishlist_button, name='add_to_wishlist_button'),
    path('remove_from_wishlist/<slug:slug>/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    
]