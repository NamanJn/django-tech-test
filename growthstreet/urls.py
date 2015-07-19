from django.conf.urls import include, url

from django.contrib import admin

from growthstreet import views



urlpatterns = [

    #url(r"^$", views.indexView, name="ViewIndex"),
    #url(r"^(?P<whichOne>(profile|))$", views.homeView, name="ViewData"),
    url(r"^$", views.homeView, name="ViewData"),
    #url(r"^profile$", views.homeView, name="ViewData"),
    # url(r"^signUp/$", views.signUpView, name="ViewSignUp"),
    url(r"^settings/$", views.settingsView, name="ViewSettings"),

    url(r"^(?P<whichOne>(signUpDone|loggedOut))/$", views.signUpDoneView, name="ViewSignUpDone"),
    url(r"^home/requestNew/$", views.dataAddView, name="ViewDataAdd"),
    url(r"^home/(?P<TEMPLATE_ID>\d+)/$", views.IDView, name="ViewID"),

    # url(r"^thank_you/$", views.thankYouView, name="ViewThankYou"),
    url(r'^', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),

]
