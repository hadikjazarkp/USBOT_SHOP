from django.shortcuts import render
from django.views import View
from .models import *
from Store.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class WishlistView(View):
    @method_decorator(login_required(login_url='loginpage'))  # Redirect to the login page if not authenticated
    def get(self, request):
        # wishlist, created = WishlistModel.objects.get_or_create(user=request.user)
        # if wishlist is not None and wishlist.product is not None:
        #     wishlist_items = wishlist.product.all()
        # else:
        #     wishlist_items = []
        # print(wishlist_items)
        
        wishlist_items = WishlistModel.objects.filter(user=request.user)
        
        return render(request, 'store/products/wishlist.html', {'wishlist_items': wishlist_items})

class AddToWishlistView(View):
    @method_decorator(login_required(login_url='loginpage'))
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        wishlist, created = WishlistModel.objects.get_or_create(user=request.user,product=product)
        print(wishlist)
        # wishlist.product.add(product)
        messages.success(request, "Your Add to Wishlist has been successfully")
        return redirect('wishlist_view')

class RemoveFromWishlistView(View):
    @method_decorator(login_required(login_url='loginpage'))
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        wishlist = WishlistModel.objects.get(user=request.user,product=product)
        wishlist.delete()
        # wishlist.product.remove(product)
        return redirect('wishlist_view')
    
    
# class add_to_wishlist_button(View):
#     @method_decorator(login_required(login_url='loginpage'))
#     def post(self, request, slug):
#         try:
#             product = get_object_or_404(Product, slug=slug)
#             wishlist, created = WishlistModel.objects.get_or_create(user=request.user,product=product)
#             if created:
#                 message = "Product added to cart successfully"
#             else:
#                 message = "Product already in the cart"

#             return JsonResponse({'success': True, 'message': message})
#         except Variant.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)

def add_to_wishlist_button(request, slug):
    try:
         product = get_object_or_404(Product, slug=slug)
         wishlist, created = WishlistModel.objects.get_or_create(user=request.user,product=product)
         if created:
             message = "Product added to cart successfully"
         else:
             message = "Product already in the cart"

         return JsonResponse({'success': True, 'message': message})
    except Variant.DoesNotExist:
         return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
