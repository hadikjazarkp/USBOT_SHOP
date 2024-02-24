from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
# from paypal.standard.forms import PayPalEncryptedPaymentsForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import stripe
import time
from django.http import HttpResponse
import random
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control



from django.shortcuts import render
from .models import Main_Images, Category, Product
@cache_control(no_cache=True, no_store=False)
def home(request):
    main_images = Main_Images.objects.first()
    category = Category.objects.all()
    all_products = Product.objects.all()

    # Create a new variable containing the first 6 products, sorted by creation date
    six_products = all_products.order_by('created_at')[:6]

    return render(request, "store/index.html", {'main_images': main_images, 'category': category, 'product': all_products, 'six_products': six_products})



def my_view(request):
    return render(request, 'my_template.html')


def shop(request):
    category = Category.objects.all()
    sub_category = Sub_Category.objects.all()
    sort_by = request.GET.get('sort')
    
    category_by = request.GET.get('category')
    search_key = request.GET.get('search')
        
    
    image = Image.objects.first()  # Get the first image object from the database
    image_url = image.image.url if image else None  # Get the URL of the image if available

    
    
    
    
    products = Product.objects.all()

    if sort_by == 'new':
        # Sort the products by the created_at attribute of their variants
        products = products.order_by('-variants__created_at')
    elif sort_by == 'low_to_high':
        # Sort the products by the selling_price attribute of their variants
        products = products.annotate(min_price=models.Max('variants__selling_price')).order_by('min_price')
    elif sort_by == 'high_to_low':
        # Sort the products by the selling_price attribute of their variants in reverse order
        products = products.annotate(max_price=models.Max('variants__selling_price')).order_by('-max_price')
    if category_by:
        products = products.filter(sub_category__category__slug = category_by)  
    if search_key:
        products = Product.objects.filter( Q(variants__color__istartswith=search_key) | Q(name__istartswith=search_key) | Q(sub_category__category__name__istartswith=search_key) | Q(sub_category__name__istartswith=search_key) ) 
        # products = [product.variants.first() for product in products]   
   
    context = {
        'category':category,
        'sub_category' : sub_category,
        'products' :products,
        'image_url': image_url,
        }
    return render(request, "store/shop.html", context)





@login_required
def settingsview(request):
    # Assuming the user is logged in, you can access the UserProfile through request.user
    user= request.user
    user_address = Address.objects.filter(user=request.user)
    first_address = Address.objects.filter(user=request.user).first()
    return render(request, 'store/auth/settings.html', {'user_profile': user, 'user_address':user_address,'first_address':first_address})



def categoryview(request,slug):
    print(slug)
    template="store/products/category.html"
    
    category=Category.objects.get(slug=slug)

   
    context={
        "category":category
       
    }
    return render(request,template,context)




def productview(request, pslug, vslug):
    template="store/products/product_view.html"
 
    
    product = Product.objects.get(slug=pslug)
    variant = Variant.objects.get(product=product,slug=vslug)
    
    
    context={
        'variant' : variant
        
       
    }
    return render(request,template,context)




@login_required(login_url='loginpage')  # Specify the login URL
def cart(request):

        
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = 0
    for item in cart_items:
        
        cart_total=cart_total+item.total_price
     
     
    
    
    return render(request, 'store/products/cart.html', {'cart_items':cart_items, 'cart_total':cart_total,} )
      
     
def cart_count_increase(request, id):
    cart_item = Cart.objects.get(id=id)
    print(cart_item.variant.quantity)
    if cart_item.variant_qty < 10:
        if cart_item.variant.quantity > cart_item.variant_qty:
            cart_item.variant_qty += 1
            cart_item.save()
        else:
            messages.error(request,"Out of Stock")    
   
    else:
        messages.error(request,"Only 10 Iteams can be added")    
        
  
    return redirect('cart_page')     
     
     
def cart_count_decrease(request, id):
    
    cart_item = Cart.objects.get(id=id)
    if cart_item.variant_qty > 1:
       cart_item.variant_qty -= 1
       cart_item.save()
    else:
        cart_item.delete()
        
        
    
    return redirect('cart_page')     
          
     
@login_required(login_url='loginpage')  # Specify the login URL
def add_to_cart(request, slug ):
    print("fghnh")
    
    variant = Variant.objects.get(slug=slug)
    cart_iteam = Cart.objects.get_or_create(variant=variant, user=request.user)
    return redirect('cart_page')


@login_required(login_url='loginpage')
def add_to_cart_button(request, slug):
    print("5uktytj")
    try:
        variant = Variant.objects.get(slug=slug)
        cart_item, created = Cart.objects.get_or_create(variant=variant, user=request.user)
        messages.success(request, "Your Add to Cart has been successfully")
        if created:
            message = "Product added to cart successfully"
        else:
            message = "Product already in the cart"

        return JsonResponse({'success': True, 'message': message})
    except Variant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)


# def add_to_cart_button(request, slug ):
    
#     print(slug)
    
#     variant = Variant.objects.get(slug=slug)
    
#     cart_iteam = Cart.objects.get_or_create(variant=variant, user=request.user)
#     messages.success(request, "Your Product added has been placed successfully") 
    
#     return redirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required
def remove_from_cart(request, slug):
    print(slug)
    try:
        item = get_object_or_404(Cart, slug=slug, user=request.user)
        print(item)
        item.delete()
        messages.success(request, "Your product has been removed from the cart successfully")
        return JsonResponse({'success': True, 'message': 'Item removed successfully'})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
  
                                                    
# @login_required
# def checkout(request):

#     cart_items = Cart.objects.filter(user=request.user)
#     cart_total = 0
#     user_address = Address.objects.filter(user=request.user)
    
#     final_price = 0
    
    
#     for item in cart_items:
        
#         cart_total=cart_total+item.total_price
     
     
#     promocodes = PromoCode.objects.filter(purchase_price__lte=cart_total)
#     discount_price = 0
#     if request.session.get('discount'):
#         print("session price")
#         discount_price = request.session.get('discount')
#         del request.session['discount']   
#     else:
#         print("not session")
#     print(discount_price)
#     final_price = cart_total - discount_price

#     client =razorpay.Client( auth = (settings.KEY, settings.SECRET))
#     payment = client.order.create({'amount': (final_price) * 100, 'currency': 'INR', 'payment_capture': 1 }) 
#     item.rezor_pay_order_id = payment['id']
#     item.save()



#     return render(request, 'store/products/checkout.html', {'cart_items':cart_items, 'cart_total':cart_total, 'promocodes':promocodes, 'user_address':user_address, 'final_price':final_price, 'discount_price':discount_price, 'payment':payment})   



@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = sum(item.total_price for item in cart_items)
    user_address = Address.objects.filter(user=request.user)

    final_price = cart_total

    promocodes = PromoCode.objects.filter(purchase_price__lte=cart_total)
    
    discount_price = 0

    if request.session.get('discount'):
        print("session price")
        discount_price = request.session.get('discount')
        del request.session['discount']
    else:
        print("not session")

    print(discount_price)
    final_price -= discount_price

    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    payment = client.order.create({'amount': final_price * 100, 'currency': 'INR', 'payment_capture': 1})
    item = cart_items.first()  # Assuming you are working with the first item in the cart
    item.rezor_pay_order_id = payment['id']
    item.save()

    # Add the Stripe publishable key to the context
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'promocodes': promocodes,
        'user_address': user_address,
        'final_price': final_price,
        'discount_price': discount_price,
        'payment': payment,
        'key': stripe_publishable_key,
    }

    return render(request, 'store/products/checkout.html', context)

# from django.http import HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt
# import razorpay
# import json

# @csrf_exempt
# def checkout(request):
#     if request.method == 'POST':
#         # Parse the Razorpay webhook payload
#         raw_data = request.body.decode('utf-8')
#         payload = json.loads(raw_data)

#         # Verify the signature
#         client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
#         try:
#             client.utility.verify_webhook_signature(raw_data, request.headers['X-Razorpay-Signature'])
#         except razorpay.errors.SignatureVerificationError:
#             return HttpResponseBadRequest('Invalid signature')

#         # Process the webhook event
#         event_type = payload['event']
#         if event_type == 'payment.captured':
#             # Payment captured, update your database or send email notifications
#             # Access relevant data from payload, such as payment ID, order ID, etc.
#             print("dghdgbdgb")
#             messages.success(request,"payment caputred")
            
#         elif event_type == 'order.paid':
#             # Order paid, update your database or trigger fulfillment process
#             # Access relevant data from payload, such as order ID, amount, etc.
#             print("dgdsgbdgbdgbgndgfngnfgnfn")
#             messages.success(request,"hgdbdfgfb")
#         # Add more event handlers as needed

#         return HttpResponse('Webhook received', status=200)

#     else:
#         # Handle GET request for rendering checkout page
#         cart_items = Cart.objects.filter(user=request.user)
#         cart_total = sum(item.total_price for item in cart_items)
#         user_address = Address.objects.filter(user=request.user)

#         final_price = cart_total

#         promocodes = PromoCode.objects.filter(purchase_price__lte=cart_total)
#         discount_price = 0

#         if request.session.get('discount'):
#             discount_price = request.session.get('discount')
#             del request.session['discount']

#         final_price -= discount_price

#         client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
#         payment = client.order.create({'amount': final_price * 100, 'currency': 'INR', 'payment_capture': 1})
#         item = cart_items.first()  # Assuming you are working with the first item in the cart
#         item.rezor_pay_order_id = payment['id']
#         item.save()

#         # Add the Stripe publishable key to the context
#         stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
#         context = {
#             'cart_items': cart_items,
#             'cart_total': cart_total,
#             'promocodes': promocodes,
#             'user_address': user_address,
#             'final_price': final_price,
#             'discount_price': discount_price,
#             'payment': payment,
#             'key': stripe_publishable_key,
#         }

#         return render(request, 'store/products/checkout.html', context)

def add_address(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone_number = request.POST.get('phone_number')  # Updated to match the HTML form
        pincode = request.POST.get('pincode') 
        address_type = request.POST.get('address_type')

        # Print the values for testing
        Address.objects.create(first_name=first_name,last_name=last_name,address=address,city=city,state=state,phone_number=phone_number,pincode=pincode,address_type=address_type, user=request.user)
        print(first_name, last_name, address, city, state, phone_number,pincode, address_type)
        messages.success(request, "Your Address has been Created successfully")

        # Perform any additional processing or save to the database as needed

    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the referring page or home if not available


def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        # Process the form data if needed, you can access it using request.POST
        # Update the address fields accordingly
        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.address_type = request.POST.get('address_type')
        address.address = request.POST.get('address')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.phone_number = request.POST.get('phone_number')
        address.pincode = request.POST.get('pincode')
        
        # Save the updated address
        address.save()
        
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    # if request.method == 'POST':
    address.delete()
    messages.success(request, "Your Address has been Deleted")
        
    return redirect(request.META.get('HTTP_REFERER', '/'))


  
def promocode_view(request):
    if request.method == 'POST':
        # Retrieve the promo code value and cart total from the POST data
        promocode_value = request.POST.get('promocodevalue')
        promocode_value = promocode_value.strip()
        print("promocode value =", promocode_value)
        promocode = PromoCode.objects.filter(code=promocode_value).first()

        disprice = promocode.discount_price
        cart_total_price = request.POST.get('cart_total')
        print("cart total price =", cart_total_price)
        
        # Validate if promo code value is provided
        if disprice is not None:
            try:
                # Assuming you want to calculate a discount based on the promo code value
                discount = float(disprice)
                
                # Add your logic to calculate the final total based on the discount and cart total
                calculated_final_total = float(cart_total_price) - discount

                # Store the discount value and promo code value in the session
                request.session['discount'] = discount
                request.session['promocode_value'] = promocode_value
                
                # Prepare the response data including promocode_value
                response_data = {
                    'discount': discount,
                    'finalTotal': calculated_final_total,
                    'promocode_value': promocode_value,
                    # Add other necessary data
                }

                # Return a JSON response with the calculated values
                return JsonResponse(response_data)
            except ValueError:
                # Handle the case where the promo code value is not a valid float
                return JsonResponse({'error': 'Invalid promo code value'})
        else:
            # If no promo code value is provided or found, return an appropriate response
            return JsonResponse({'error': 'Invalid promo code'})
    else:
        # Handle the case where the request method is not POST
        return JsonResponse({'error': 'Invalid request method'})




@login_required
def placeorder(request):
    if request.method == 'POST':
        # neworder = Order()
        # neworder.user = request.user
        try:
            address = request.POST.get('selectedAddressId').strip()
            address = Address.objects.get(id=address)
        
        
            payment_mode = request.POST.get('payment_mode')
            total_price = request.POST.get('finalTotal')
            coupon=request.POST.get('discount_price')
            print(coupon)
            # # Ensure that the tracking number is unique
            trackno = 'usbot' + str(random.randint(1111111, 9999999))
            while UserOrder.objects.filter(tracking_no=trackno).exists():
                trackno = 'usbot' + str(random.randint(1111111, 9999999))
            
            # neworder.tracking_no = trackno
            # neworder.save()
            neworder= UserOrder.objects.create(user=request.user,address=address,total_price=total_price,payment_mode=payment_mode,tracking_no=trackno)
            neworderitems = Cart.objects.filter(user=request.user)
            print(total_price)

            for item in neworderitems:
                UserOrderItem.objects.create(
                    order=neworder,
                    variant=item.variant,
                    quantity=item.variant_qty,
                    price=item.variant.selling_price,
                    total=total_price,
                    coupon=coupon
                    
                )    

                # To decrease the product quantity from available stock
                orderproduct = Variant.objects.get(id=item.variant.id)
                orderproduct.quantity = orderproduct.quantity - item.variant_qty
                orderproduct.save()
                Cart.objects.filter(user=request.user).delete()  
        
                messages.success(request, "Your order has been placed successfully")  

                return redirect('home')
        except:
            messages.error(request, "Please add atleast one address")
            return redirect(request.META.get('HTTP_REFERER', '/'))
                

        # To clear user Cart



def profile_view(request):
    
    return render(request, 'store/auth/profile.html',)
    
from django.core.paginator import Paginator

def profile_order(request):
    orders = UserOrder.objects.filter(user=request.user)

    # Pagination
    paginator = Paginator(orders, 5)  # Show 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'orders': page_obj}
    return render(request, 'store/auth/order.html', context)


def profile_address(request):
    user= request.user
    user_address = Address.objects.filter(user=request.user)
    first_address = Address.objects.filter(user=request.user).first()
    return render(request, 'store/auth/address.html', {'user_profile': user, 'user_address':user_address,'first_address':first_address})




def edit_profile(request):
    if request.method == "POST":
        profile_image=request.FILES.get("profile_image")
        print(profile_image)
        user=request.user
        print(user)
        
        user.profile_image=profile_image
        user.save()
        messages.success(request, "Your Address has been Edited ")
    return redirect(request.META.get('HTTP_REFERER', '/'))
        


# def charge(request):
#     if request.method == 'POST':
#         charge = stripe.Charge.create(
#             amount=500,
#             currency='inr',
#             description='A Django charge',
#             source=request.POST['stripeToken']
#         )

def charge(request):
    if request.method == 'POST':
        
            # Set your Stripe secret key
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # Create a charge
            charge = stripe.Charge.create(
                amount=500,
                currency='inr',
                description='payment ',
                source=request.POST['stripeToken']
            )

            # If the charge was successful, return a success message
            return JsonResponse({'message': 'Payment successful!'})

        # except stripe.error.CardError as e:
        #     # The card has been declined
        #     return JsonResponse({'error_message fff': str(e)}, status=400)
        # except Exception as e:
        #     # An error occurred during the payment process
        #     return JsonResponse({'error_message fdt': str(e)}, status=500)

    # Handle cases where the request method is not POST
    return JsonResponse({'error_messagedghgh': 'Invalid request method'}, status=400)

        
    

