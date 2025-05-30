from django.urls import path
from . import views
from .views import ShippingAddressView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("products", views.products, name="products"),
    path("product_detail/<slug:slug>", views.product_detail, name="product_detail"),
    path("add_item/", views.add_item, name="add_item"),
    path("product_in_cart", views.product_in_cart, name="product_in_cart"),
    path("get_cart_stat", views.get_cart_stat, name="get_cart_stat"),
    path("get_cart", views.get_cart, name="get_cart"),
    path("update_quantity/", views.update_quantity, name="update_quantity"),
    path("delete_cartitem/", views.delete_cartitem, name="delete_cartitem"),
    path("get_username", views.get_username, name="get_username"),
    path("user_info", views.user_info, name="user_info"),
    path("initiate_payment/", views.initiate_payment, name="initiate_payment"),
    path("payment_callback", views.payment_callback, name="payment_callback"),
    path('api/shipping/', ShippingAddressView.as_view(), name='shipping-address'),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#fetching all_products: http://127.0.0.1:8000/products



