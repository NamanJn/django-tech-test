from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('growthstreetApp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls'))

]
