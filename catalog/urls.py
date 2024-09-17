from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactView, ProductDetailView, PostListView, PostDetailView, PostCreateView, \
    PostUpdateView, PostDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('blog/', PostListView.as_view(), name='posts'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('blog/create', PostCreateView.as_view(), name='post_create'),
    path('blog/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('blog/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete')
]
