
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import urlresolvers
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from growthstreet.models import LoanRequest, UserDetails
from growthstreet.forms import LoanRequestForm, UserDetailsForm

from django.contrib import auth
import pdb

def login_needed(myfunc):

    def inner(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return HttpResponseRedirect(urlresolvers.reverse("auth_login"))
        return myfunc(*args, **kwargs)

    return inner


def indexView(request):

    context = {}
    context["wrongCredentials"] = 0

    if request.user.is_authenticated():
        return HttpResponseRedirect(urlresolvers.reverse("auth_login"))

    if request.method == "POST":

        dusername = request.POST["username"]
        dpassword = request.POST["password"]
        loginTry = auth.authenticate(username=dusername, password=dpassword);

        if loginTry is not None:
            auth.login(request, loginTry);
            return HttpResponseRedirect(urlresolvers.reverse("ViewData"));

        else:
            context["wrongCredentials"] = -1

    theForm = AuthenticationForm()
    context["theForm"] = theForm
    return render(request, "growthstreetApp/index.html", context)

def signUpView(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(urlresolvers.reverse("growthstreetApp:ViewIndex"))

    context = {}

    if request.method == "POST":
        theForm = UserCreationForm(request.POST)

        if theForm.is_valid():
            theForm.save()
            return HttpResponseRedirect(urlresolvers.reverse("ViewSignUpDone", args=("signUpDone",)))
        else:
            print "These are the errors shown below \n"
            print theForm.errors

            tempo = []
            for i in theForm.errors.values():
                tempo += i
            context["formError"] =tempo[0]

    context["theForm"] = UserCreationForm()
    return render(request, "growthstreetApp/signUp.html", context);

def signUpDoneView(request,whichOne):

    context={}
    if whichOne == "signUpDone":
        context["display"] = "signed up";

    elif whichOne == "loggedOut":
        context["display"] = "logged out";
        auth.logout(request)
        return HttpResponseRedirect(urlresolvers.reverse("auth_login"))

    return render(request, "growthstreetApp/signUpDone.html", context)



@login_needed
def homeView(request):

    templateID = request.GET.get('delete', None);

    if templateID:
        formTemplates = request.user.loanrequest_set.all()
        try:
            templateToDelete = formTemplates[int(templateID)-1]
        except:
            return HttpResponseRedirect(urlresolvers.reverse("ViewData"))
        print "this is the template to be deleted", templateToDelete

        templateToDelete.delete() # deleting the webform
        return HttpResponseRedirect(urlresolvers.reverse("ViewData"))


    context = {}
    formTemplates = request.user.loanrequest_set.all()

    context["theData"] = formTemplates
    theFields = LoanRequest._meta.fields[1:-1]
    context["theTitles"] = theFields
    context['request'] = request.build_absolute_uri()[:-1]

    hostName = request.META['HTTP_HOST']
    context['hostName'] = hostName

    return render(request, "growthstreetApp/formTemplates.html", context)

@login_needed
def dataAddView(request):

    context = {}
    context["wrongCredentials"] = 1

    context["whatData"] = "events"

    if request.method == "POST":

        print request.POST
        form = LoanRequestForm(request.POST)

        if form.is_valid():
            # creating and saving the webform object.
            templateObject = form.save(commit=False)
            templateObject.user = request.user
            templateObject.save()

            return HttpResponseRedirect(urlresolvers.reverse("ViewData"));

        else:
            print form.errors
            print "This is the form data", form.data
            context["wrongCredentials"]= -1
            print "This is the form invalid", form.as_p();

    else:
        form = LoanRequestForm()

    context["form"] = form
    return render(request, "growthstreetApp/formTemplateAdd.html", context)

@login_needed
def IDView(request, TEMPLATE_ID):

    events = request.user.loanrequest_set.all()
    context = {}
    # note that TEMPLATE_ID is a string variable and not an int
    if int(TEMPLATE_ID) <= len(events) and int(TEMPLATE_ID) > 0:

        display = None

        selectedData = events[int(TEMPLATE_ID)-1]

        if request.method == "POST":

            form = LoanRequestForm(request.POST, instance=selectedData)

            if form.is_valid():

                form.save()
                display = "You have successfully updated the event !"
                #context["display"] = display

                return HttpResponseRedirect(urlresolvers.reverse("growthstreetApp:ViewID", args=(TEMPLATE_ID,)))
                #return render(request, "growthstreetApp/templatesID.html", context)

        else:
            form = LoanRequestForm(instance=selectedData)

    else:
        return HttpResponseNotFound("<h1>Sorry page not found ! </h1>")


    context["form"] = form
    context["display"] = display
    context["TemplateID"] = TEMPLATE_ID

    return render(request, "growthstreetApp/templatesID.html", context)


def thankYouView(request):
    context = {}
    return render(request, "growthstreetApp/thankYou.html", context)


@login_needed
def settingsView(request):

    context = {}
    userDetails = UserDetails.objects.filter(user=request.user)

    if request.method == "POST":

        if len(userDetails) >= 1:
            userDetail = userDetails[0]
            form = UserDetailsForm(request.POST, instance=userDetail)

        else:
            form = UserDetailsForm(request.POST)

        if form.is_valid():
            # creating and saving the webform object.
            templateObject = form.save(commit=False)
            templateObject.user = request.user
            templateObject.save()

            return HttpResponseRedirect(urlresolvers.reverse("ViewSettings"))

        else:
            context["wrongCredentials"]= -1
    else:

        if len(userDetails) >= 1:
            userDetail = userDetails[0]
            form = UserDetailsForm(instance=userDetail)
        else:
            form = UserDetailsForm(initial={'userEmail': request.user.email})
            

    return render(request, "growthstreetApp/settings.html", {"form": form})