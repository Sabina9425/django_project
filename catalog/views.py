from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.models import Product, Post


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    fields = ("header", "content", "preview")
    success_url = reverse_lazy('catalog:posts')


class PostUpdateView(UpdateView):
    model = Post
    fields = ("header", "content", "preview")
    success_url = reverse_lazy('catalog:posts')


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('catalog:posts')
