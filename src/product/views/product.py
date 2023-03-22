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

class SaveProductView(View):
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



def productList(request):
    if request.method == "GET":

        title = request.GET.get('title', "")

        variant = request.GET.get('variant', None)

        min_price = request.GET.get('price_from', None)
        max_price = request.GET.get('price_to', None)
        date = request.GET.get('date', None)


        if min_price and max_price and date:

            print(date)
            search_datetime = datetime.strptime(date, '%Y-%m-%d')

            print(search_datetime)
        
            # queryset = Product.objects.filter(date_field__date=search_datetime.date())

            product_qs = ProductVariantPrice.objects.filter(price__range=(min_price, max_price))

            # print(p_qs)

            variant_qs = ProductVariant.objects.filter(variant_title__icontains=variant)

            print("variant:", variant_qs)



            qs = Product.objects.filter(id__in=product_qs.values('product_id'))

            vs = Product.objects.filter(id__in=variant_qs.values('product_id'))

            print(qs)

            # if min_price and max_price:
            products = Product.objects.filter(
                Q(title__icontains=title) | Q(
                    created_at__date=search_datetime.date())
            ).union(
                Product.objects.filter(id__in=product_qs.values('product_id'))
            ).union(
                Product.objects.filter(id__in=variant_qs.values('product_id'))
            )
        else:
            products = Product.objects.all()

        
    else:
        products = Product.objects.all()
        
    variant_prices = ProductVariantPrice.objects.all()
    product_variants = ProductVariant.objects.values('variant_title', 'variant').distinct()
    print(product_variants)
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
