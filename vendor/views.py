from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import  UserProfileForm
from .forms import VendorForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from menu.models import Category, FoodItem
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

# def get_vendor(request):
#     vendor= Vendor.objects.get(user=request.user)
#     return vendor
# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user) 
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)

#@login_required(login_url='login')
#@user_passes_test(check_role_vendor)
# def menu_builder(request):
#     vendor = get_vendor(request)
#     categories = Category.objects.filter(vendor=vendor)
#     context={
#          'categories' : categories
#          }
#     return render(request, 'vendor/menu_builder.html',context)

class menu_builder(ListView):
    template_name = 'vendor/menu_builder.html'
    model = Category
    context_object_name = "categories"
    def get_queryset(self):
        self.vendor = get_object_or_404(Vendor, user=self.request.user)
        return Category.objects.filter(vendor=self.vendor)



# @login_required(login_url='login')
# @user_passes_test(check_role_vendor)
# def fooditems_by_category(request, pk=None):
#     vendor = get_vendor(request)
#     category = get_object_or_404(Category, pk=pk)
#     fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
#     context = {
#         'fooditems': fooditems,
#         'category': category,
#     }
#     return render(request, 'vendor/fooditems_by_category.html', context)


class fooditems_by_category(DetailView):
    model = Category
    slug_field = 'pk'
    template_name= 'vendor/fooditems_by_category.html'
    def get_queryset(self):
        self.vendor = get_object_or_404(Vendor, user=self.request.user)
        self.category = Category.objects.filter(vendor=self.vendor)
        return Category.objects.filter(vendor=self.vendor)
    def get_context_data(self, **kwargs):
        context = super(fooditems_by_category, self).get_context_data(**kwargs)
        context['category']  = Category.objects.filter(vendor=self.vendor)
        context['fooditems']  = FoodItem.objects.filter(vendor=self.vendor,category=pk)       
        return context

class add_category(CreateView):
    model=Category
    success_url = reverse_lazy("menu_builder")
    def get(self, request, *args, **kwargs):
        context = {'form': CategoryForm()}
        return render(request, 'vendor/add_category.html', context)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_object_or_404(Vendor, user=self.request.user)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect(self.success_url)
        else:
              print(form.errors)
        return render(request, 'vendor/add_category.html', {'form': form})


# def add_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             category_name = form.cleaned_data['category_name']
#             category = form.save(commit=False)
#             category.vendor = get_vendor(request)
#             category.slug = slugify(category_name)
#             form.save()
#             messages.success(request, 'Category added successfully!')
#             return redirect('menu_builder')
#         else:
#             print(form.errors)

#     else:
#         form = CategoryForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'vendor/add_category.html', context)


# def edit_category(request, pk=None):
#     category = get_object_or_404(Category, pk=pk)
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, instance=category)
#         if form.is_valid():
#             category_name = form.cleaned_data['category_name']
#             category = form.save(commit=False)
#             category.vendor = get_vendor(request)
#             category.slug = slugify(category_name)
#             form.save()
#             messages.success(request, 'Category updated successfully!')
#             return redirect('menu_builder')
#         else:
#             print(form.errors)

#     else:
#         form = CategoryForm(instance=category)
#     context = {
#         'form': form,
#         'category': category,
#     }
#     return render(request, 'vendor/edit_category.html', context)

class edit_category(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'vendor/edit_category.html'
    success_url = reverse_lazy("menu_builder")


# def delete_category(request, pk=None):
#     category = get_object_or_404(Category, pk=pk)
#     category.delete()
#     messages.success(request, 'Category has been deleted successfully!')
#     return redirect('menu_builder')

class delete_category(DeleteView):
    model = Category
    success_url = reverse_lazy("menu_builder")