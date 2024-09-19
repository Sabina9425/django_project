from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactView, ProductDetailView, PostListView, PostDetailView, PostCreateView, \
    PostUpdateView, PostDeleteView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path("product/create", ProductCreateView.as_view(), name='product_create'),
    path("product/<int:pk>/update", ProductUpdateView.as_view(), name='product_update'),
    path("product/<int:pk>/delete", ProductDeleteView.as_view(), name='product_delete'),
    path('blog/', PostListView.as_view(), name='posts'),
    path('blog/<str:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('blog/create', PostCreateView.as_view(), name='post_create'),
    path('blog/<str:slug>/update', PostUpdateView.as_view(), name='post_update'),
    path('blog/<str:slug>/delete', PostDeleteView.as_view(), name='post_delete')
]
