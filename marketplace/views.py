from django.shortcuts import get_object_or_404,render
from django.views.generic.base import TemplateView
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.views.generic import DetailView
from django.db.models import Prefetch
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

       
        return context

