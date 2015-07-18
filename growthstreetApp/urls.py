from django.conf.urls import patterns,url

from growthstreetApp import views

urlpatterns = patterns("",
    url(r"^$", views.indexView, name="ViewIndex"),
    #
    # url(r"^user_templates/$", views.dataView, name="ViewData"),
    # url(r"^signUp/$", views.signUpView, name="ViewSignUp"),
    #
    # url(r"^(?P<whichOne>(signUpDone|loggedOut))/$", views.signUpDoneView, name="ViewSignUpDone"),
    # url(r"^user_templates/add/$", views.dataAddView, name="ViewDataAdd"),
    # url(r"^email_sent/$", views.sendEmailView, name="ViewEmailSent"),
    #
    # url(r"^user_templates/(?P<TEMPLATE_ID>\d+)/$", views.IDView, name="ViewID"),
    # url(r"^user_templates/(?P<TEMPLATE_ID>\d+)/responses/$", views.responseView, name="ViewResponse"),
    # url(r"^share_templates/(?P<TEMPLATE_ID>\d+)/$", views.shareTemplateView, name="ViewShareTemplate"),
    # url(r"^preview_templates/(?P<TEMPLATE_STRING>\w+)/$", views.previewTemplateView, name="ViewPreviewTemplate"),
    # url(r"^thank_you/$", views.thankYouView, name="ViewThankYou")

)