from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='accounts:login'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

# Add Django's authentication URLs
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
