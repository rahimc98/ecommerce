from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        path('admin/', admin.site.urls),
        path("", include("web.urls", namespace="web")),
        path("products/", include("products.urls", namespace="products")),
        path("main/", include("main.urls", namespace="main")),
        path("order/", include("order.urls", namespace="order")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
admin.site.site_header = "Ecommerce Administration"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome to Ecommerce Admin Portal"