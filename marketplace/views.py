from django.shortcuts import render
from django.views.generic.base import TemplateView
from vendor.models import Vendor
# Create your views here.
class MarketPlace(TemplateView):
     template_name = "marketplace/listings.html"
    
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor_count'] = Vendor.objects.count()
        context['vendors'] =  Vendor.objects.filter(is_approved=True, user__is_active=True)
        return context
    

