from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('registration.backends.default.urls'))
    url(r'^', include('growthstreetApp.urls')),
    url(r'^admin/', include(admin.site.urls)),

]
