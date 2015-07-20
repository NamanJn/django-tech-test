from django.conf.urls import include, url

from django.contrib import admin

from growthstreet import views



urlpatterns = [

    url(r"^$", views.homeView, name="ViewData"),
    url(r"^settings/$", views.settingsView, name="ViewSettings"),

    url(r"^home/requestNew/$", views.dataAddView, name="ViewDataAdd"),
    url(r"^home/(?P<TEMPLATE_ID>\d+)/$", views.IDView, name="ViewID"),

    url(r'^', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),

]
