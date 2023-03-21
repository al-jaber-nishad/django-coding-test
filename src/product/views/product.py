from django.views import generic
from django.shortcuts import render, get_object_or_404
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListView(generic.ListView):
    model = ProductVariantPrice
    template_name = 'products/list.html'
    context_object_name = 'products'
    ordering = ['-updated_at']
    paginate_by = 2

    # def get_queryset(self):
    #     user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     return Post.objects.filter(author=user).order_by('-date_posted')

def productList(request):

    product_list = Product.objects.all()
    variants = ProductVariantPrice.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 2)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'variants': variants,
    }

    return render(request, 'products/list.html', context)