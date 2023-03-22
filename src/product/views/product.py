from django.views import generic, View
from django.shortcuts import render, get_object_or_404
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'


    def post(self, request):
        # get form data from POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        sku = request.POST.get('sku')
        
        # create a new product instance with the form data
        product = Product(title=title, description=description, sku=sku)
        
        # save the new product instance to the database
        product.save()
        
        # redirect to a success page
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

def productList(request):

    title = request.GET.get('title')
    variant = request.GET.get('variant')
    min_price = request.GET.get('price_from')
    max_price = request.GET.get('price_to')
    date = request.GET.get('date')
    end_date = request.GET.get('end_date')

    print(min_price, max_price)

    products = Product.objects.all()

    if title:
        products = products.filter(Q(title__icontains=title)).distinct()
        print('title')

    if variant:
        products = products.filter(productvariant__variant_title__icontains=variant)

    if min_price and max_price:
        print('min price')

        products = products.filter(productvariantprice__price__range=(min_price, max_price))
        print(products)
        print('after ')

    if date:
        search_datetime = datetime.strptime(date, '%Y-%m-%d').date()
        print(search_datetime)
        products = products.filter(created_at__date=search_datetime)

    print(products)
        
    variant_prices = ProductVariantPrice.objects.all()
    product_variants = ProductVariant.objects.values('variant_title', 'variant').distinct()
    variants = Variant.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 2)
    try:
        prod_paginator = paginator.page(page)
    except PageNotAnInteger:
        prod_paginator = paginator.page(1)
    except EmptyPage:
        prod_paginator = paginator.page(paginator.num_pages)

    context = {
        'prod_paginator': prod_paginator,
        'products': products,
        'variant_prices': variant_prices,
        'variants': variants,
        'product_variants': product_variants,
    }

    return render(request, 'products/list.html', context)
