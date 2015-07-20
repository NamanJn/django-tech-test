
from django.core import urlresolvers
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from growthstreet.models import LoanRequest, UserDetails
from growthstreet.forms import LoanRequestForm, UserDetailsForm, UserForm


def login_needed(myfunc):

    def inner(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return HttpResponseRedirect(urlresolvers.reverse("auth_login"))
        return myfunc(*args, **kwargs)
    return inner


@login_needed
def homeView(request):

    templateID = request.GET.get('delete', None);

    if templateID:
        formTemplates = request.user.loanrequest_set.all()
        try:
            templateToDelete = formTemplates[int(templateID)-1]
        except:
            return HttpResponseRedirect(urlresolvers.reverse("ViewData"))

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

        form = LoanRequestForm(request.POST)

        if form.is_valid():
            # creating and saving the webform object.
            templateObject = form.save(commit=False)
            templateObject.user = request.user
            templateObject.save()

            return HttpResponseRedirect(urlresolvers.reverse("ViewData"))

        else:
            context["wrongCredentials"]= -1

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

                return HttpResponseRedirect(urlresolvers.reverse("ViewID", args=(TEMPLATE_ID,)))

        else:
            form = LoanRequestForm(instance=selectedData)

    else:
        return HttpResponseNotFound("<h1>Sorry page not found ! </h1>")


    context["form"] = form
    context["display"] = display
    context["TemplateID"] = TEMPLATE_ID

    return render(request, "growthstreetApp/templatesID.html", context)


@login_needed
def settingsView(request):

    context = {}
    userDetails = UserDetails.objects.filter(user=request.user)

    if request.method == "POST":
        userform = UserForm(request.POST, instance=request.user)
        if len(userDetails) >= 1:
            userDetail = userDetails[0]
            form = UserDetailsForm(request.POST, instance=userDetail)
        else:
            form = UserDetailsForm(request.POST)

        if form.is_valid() and userform.is_valid():
            # creating and saving the webform object.
            templateObject = form.save(commit=False)
            templateObject.user = request.user
            userform.save()
            templateObject.save()

            return HttpResponseRedirect(urlresolvers.reverse("ViewSettings"))

        else:
            context["wrongCredentials"]= -1
    else:
        userform = UserForm(instance=request.user)
        if len(userDetails) >= 1:
            userDetail = userDetails[0]
            form = UserDetailsForm(instance=userDetail)
        else:
            form = UserDetailsForm()


    context = {}
    context['form'] = form
    context['userform'] = userform
    return render(request, "growthstreetApp/settings.html", context)
