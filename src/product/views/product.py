from django.views import generic
from django.shortcuts import render, get_object_or_404
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


def productList(request):
    if request.method == "GET":

        title = request.GET.get('title', "")

        # variant = request.GET.get('variant', "")

        min_price = request.GET.get('price_from', None)
        max_price = request.GET.get('price_to', None)
        date = request.GET.get('date', None)

        print(date)
        search_datetime = datetime.strptime(date, '%Y-%m-%d')

        print(search_datetime)
    
        # queryset = Product.objects.filter(date_field__date=search_datetime.date())

        p_qs = ProductVariantPrice.objects.filter(price__range=(min_price, max_price))

        print(p_qs)

        qs = Product.objects.filter(id__in=p_qs.values('product_id'))

        print(qs)

        # if min_price and max_price:
        products = Product.objects.filter(
            Q(title__icontains=title) | Q(
                created_at__date=search_datetime.date())
        ).union(
            Product.objects.filter(id__in=p_qs.values('product_id'))
        )
        
    else:
        products = Product.objects.all()
        
    variants = ProductVariantPrice.objects.all()
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
        'variants': variants,
    }

    return render(request, 'products/list.html', context)
