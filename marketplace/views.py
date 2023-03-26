from django.shortcuts import get_object_or_404,render
from django.views import View
from django.views.generic.base import TemplateView
from accounts.models import User
from marketplace.context_processors import get_cart_counter
from marketplace.models import Cart
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.views.generic import DetailView,CreateView,DeleteView
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
class MarketPlace(TemplateView):
     template_name = "marketplace/listings.html"
    
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor_count'] = Vendor.objects.count()
        context['vendors'] =  Vendor.objects.filter(is_approved=True, user__is_active=True)
        return context
    
class VendorDetail(DetailView):
   model= Vendor
   slug_url_kwarg = 'vendor_slug'
   slug_field = 'vendor_slug'
  
   template_name='marketplace/vendor_detail.html'
   
   def get_context_data(self, **kwargs):
        vendor=get_object_or_404(Vendor, vendor_slug=self.kwargs['vendor_slug'])
        context = super(VendorDetail, self).get_context_data(**kwargs)  
        context['vendor']  = vendor
        context['categories']= Category.objects.filter(vendor=vendor).prefetch_related(Prefetch(

         'fooditems',
         queryset=FoodItem.objects.filter(is_available=True)

         ))
        if self.request.user.is_authenticated:
            context['cart_items']=Cart.objects.filter(user=self.request.user)

       
        return context


# def add_to_cart(request, food_id):
#    return HttpResponse('Testing')

class AddToCart(View):
      def get(self, request, *args, **kwargs):
        # Perform io-blocking view logic using await, sleep for example.
        if request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
              try:
                 fooditem = get_object_or_404(FoodItem, id=self.kwargs['food_id'])
                 #print(fooditem)
                # Check if the user has already added that food to the cart
                 try:
                    
                     chkCart = get_object_or_404(Cart, user=self.request.user, fooditem=fooditem)
                      # Increase the cart quantity
                     chkCart.quantity += 1
                     chkCart.save()
                     return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(self.request), 'qty': chkCart.quantity})
                 except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(self.request), 'qty': chkCart.quantity})
              except:
                 return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
            else:
              return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

        else:
          return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

class DecreaseCart(View):
    def get(self, request, *args, **kwargs):
        # Perform io-blocking view logic using await, sleep for example.
        if request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
              try:
                 fooditem = get_object_or_404(FoodItem, id=self.kwargs['food_id'])
                 #print(fooditem)
                # Check if the user has already added that food to the cart
                 try:
                    
                     chkCart = get_object_or_404(Cart, user=self.request.user, fooditem=fooditem)
                      # Increase the cart quantity
                     chkCart.quantity -= 1
                     chkCart.save()
                     return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(self.request), 'qty': chkCart.quantity})
                 except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
              except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
            else:
             return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

        else:
          return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
# # inside CreateView class
# class AddToCart(CreateView):
#    model=Cart
#    def get_form_kwargs(self):
#     kwargs = super(AddToCart, self).get_form_kwargs()
#     kwargs['food_id'] = self.kwargs.get('Food_Id')
#     return kwargs

#    def render_to_response(self, context, **response_kwargs):
    # """ Allow AJAX requests to be handled more gracefully """
    # if self.request.user.is_authenticated:
    #     if self.request.is_ajax():
    #         try:
    #             fooditem = FoodItem.objects.get(id=self.kwargs.get('Food_Id'))
    #             # Check if the user has already added that food to the cart
    #             try:
    #                 chkCart = Cart.objects.get(user=self.request.user, fooditem=fooditem)
    #                 # Increase the cart quantity
    #                 chkCart.quantity += 1
    #                 chkCart.save()
    #                 return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
    #             except:
    #                 chkCart = Cart.objects.create(user=self.request.user, fooditem=fooditem, quantity=1)
    #                 return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
    #         except:
    #             return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
    #     else:
    #         return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

    # else:
    #   return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@login_required(login_url='login')
def cart(request):
  cart_items=Cart.objects.filter(user=request.user)
  print('ya ali',cart_items)
  context={
    'cart_items':cart_items,
  }
  return render(request,'marketplace/cart.html',context)

def delete_cart(request,cart_id):
        if request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
              try:
                 cart_item = Cart.objects.get(user=request.user,id=cart_id)
                 
                 if cart_item:
          
                      cart_item.delete()
                      return JsonResponse({'status': 'Success', 'message': 'Cart Item has been deleted!','cart_counter': get_cart_counter(request)})
              except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
            else:
             return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

        else:
           return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
      