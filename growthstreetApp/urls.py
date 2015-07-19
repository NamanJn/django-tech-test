from django.conf.urls import patterns,url

from growthstreetApp import views

urlpatterns = patterns("",
    url(r"^$", views.indexView, name="ViewIndex"),
    #
    url(r"^home/$", views.homeView, name="ViewData"),
    url(r"^signUp/$", views.signUpView, name="ViewSignUp"),
    url(r"^settings/$", views.settingsView, name="ViewSettings"),

    url(r"^(?P<whichOne>(signUpDone|loggedOut))/$", views.signUpDoneView, name="ViewSignUpDone"),
    url(r"^home/requestNew/$", views.dataAddView, name="ViewDataAdd"),

    url(r"^home/(?P<TEMPLATE_ID>\d+)/$", views.IDView, name="ViewID"),
    url(r"^thank_you/$", views.thankYouView, name="ViewThankYou")

)