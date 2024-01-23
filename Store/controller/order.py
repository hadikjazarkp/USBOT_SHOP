from django.shortcuts import render,redirect
from Store.models import *
from Store.forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from paypal.standard.forms import PayPalEncryptedPaymentsForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import stripe
import time
from django.http import HttpResponse
import random
from xhtml2pdf import pisa 
from xhtml2pdf import pdf
from django.http import HttpResponse
from django.template.loader import get_template,render_to_string
from django.views import View





def index(request):
    orders = UserOrder.objects.filter(user=request.user)
    context = { 'order':orders }
    return render(request, "store/order/index.html", context)

def orderview(request, t_no):
    order = UserOrder.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems=UserOrderItem.objects.filter(order=order)
    context = {
        'order':order,
        'orderitems':orderitems
    }
    return render(request,'store/order/view.html', context)
    
def delete_order(request, pk):
    """ Cancel an order from the profile page """
    order = UserOrder.objects.filter(id=pk).first()
    print(order.status)
    if request.method == "GET":
        order.status = "Cancelled"
        order.save()
        

    return redirect(request.META.get('HTTP_REFERER', '/'))    



class UserInvoice(View):
  def get(self, request, id):
    template_name = 'store/order/invoice.html'
    order = request.user.userorder.get(id=id)
    context = {'order':order}
    html_content = render_to_string(template_name, context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response,encoding='utf-8')
    if pisa_status:
      return response
    return None