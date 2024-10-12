from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Post, Version, Category


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


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView, LoginRequiredMixin):
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

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_edit_category") and user.has_perm("catalog.can_edit_publish") and user.has_perm(
                "catalog.can_edit_description"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(DeleteView, LoginRequiredMixin):
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


class CategoryListView(ListView):
    model = Category


class CategoryCreateView(CreateView):
    model = Category
    fields = ("name", "description")
    success_url = reverse_lazy('catalog:categories')

    def form_valid(self, form):
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.slug = slugify(new_category.name)
            new_category.save()

        return super().form_valid(form)


class CategoryUpdateView(UpdateView, LoginRequiredMixin):
    model = Category
    fields = ("name", "description")
    success_url = reverse_lazy('catalog:categories')


class CategoryDeleteView(DeleteView, LoginRequiredMixin):
    model = Category
    success_url = reverse_lazy('catalog:categories')
