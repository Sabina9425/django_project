from django.forms import inlineformset_factory
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Post, Version


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        active_versions = {}

        # Iterate through each product and fetch its current version
        for product in products:
            current_version = product.versions.filter(is_current_version=True).first()
            if current_version:
                active_versions[product.id] = current_version

        # Add the active versions to the context
        context['active_versions'] = active_versions
        return context


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data["formset"] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    model = Post
    fields = ("header", "content", "preview")
    success_url = reverse_lazy('catalog:posts')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.header)
            new_blog.save()

        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    fields = ("header", "content", "preview")
    success_url = reverse_lazy('catalog:posts')

    def get_success_url(self):
        return reverse('catalog:post_detail', args=[self.kwargs.get('slug')])


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('catalog:posts')
