from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import urlresolvers
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
#from LearniumApp.models import FormTemplate, FormField, AddFormTemplateFormx, AddFormFieldFormx,FormResponse
from django.contrib import auth
from django.core.mail import EmailMultiAlternatives
import pdb
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
#from LearniumApp import personalfunctions

from collections import Counter

def login_needed(myfunc):

    def inner(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return HttpResponseRedirect(urlresolvers.reverse("auth_login"))
        return myfunc(*args, **kwargs)

    return inner

@login_needed
def indexView(request):

    theContext = {}
    theContext["wrongCredentials"] = 0


    if request.method =="POST":

        dusername = request.POST["username"]
        dpassword = request.POST["password"]
        loginTry = auth.authenticate(username=dusername, password=dpassword);

        if loginTry is not None:
            auth.login(request, loginTry);
            return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewData"));

        else:
            theContext["wrongCredentials"] = -1

    theForm = AuthenticationForm()
    theContext["theForm"] = theForm
    return render(request, "LearniumApp/index.html", theContext)

def signUpView(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewIndex"))

    theContext={}

    if request.method == "POST":
        theForm = UserCreationForm(request.POST)

        if theForm.is_valid():
            theForm.save()
            return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewSignUpDone", args=("signUpDone",)))
        else:
            print "These are the errors shown below \n"
            print theForm.errors

            tempo = []
            for i in theForm.errors.values():
                tempo += i
            theContext["formError"] =tempo[0]


    theContext["theForm"] = UserCreationForm()
    return render(request, "LearniumApp/signUp.html", theContext);

def signUpDoneView(request,whichOne):

    theContext={}
    if whichOne == "signUpDone":
        theContext["display"] = "signed up";

    elif whichOne == "loggedOut":
        theContext["display"] = "logged out";
        auth.logout(request)
        return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewIndex"))

    return render(request, "LearniumApp/signUpDone.html", theContext)



@login_needed
def dataView(request):


    templateID = request.GET.get('delete', None);
    if templateID:
        formTemplates = request.user.formtemplate_set.all()
        try:
            templateToDelete = formTemplates[int(templateID)-1]
        except:
            return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewIndex"))
        print "this is the template to be deleted", templateToDelete

        for i in templateToDelete.formfield_set.all(): i.delete() # deleting the form fields
        templateToDelete.delete() # deleting the webform
        return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewIndex"))


    theContext = {}
    formTemplates = request.user.formtemplate_set.all()

    theContext["theData"] = formTemplates;
    theFields = FormTemplate._meta.fields[1:-2]; # don't want to display the url and user.
    theContext["theTitles"] = theFields
    theContext['request'] = request.build_absolute_uri()[:-1]
    hostName = request.META['HTTP_HOST']
    print hostName
    theContext['hostName'] = hostName
    return render(request, "LearniumApp/formTemplates.html", theContext)

@login_needed
def dataAddView(request):

    theContext = {}
    theContext["wrongCredentials"] = 1

    theContext["whatData"] = "events"
    #formTemplateSet= inlineformset_factory(FormTemplate, FormField)

    if request.method == "POST":
        print request.POST
        fieldFormSet = formset_factory(AddFormFieldFormx)
        templateForm = AddFormTemplateFormx(request.POST);
        formset = fieldFormSet(request.POST)

        if templateForm.is_valid() and formset.is_valid():
            # creating and saving the webform object.
            templateObject = templateForm.save(commit=False)
            templateObject.ownedBy = request.user;
            randomString = personalfunctions.generateRandom();
            templateObject.url = randomString
            print 'http://localhost:8000/preview_templates/'+randomString
            templateObject.save();

            for form in formset.forms:
                fieldObject = form.save(commit=False)
                fieldObject.ownedByWhichTemplate = templateObject;
                fieldObject.save()

            return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewIndex"));

        else:
            print templateForm.errors
            print "This is the form data", templateForm.data
            theContext["wrongCredentials"]= -1
            print "This is the form invalid", templateForm.as_p();

    else:
        fieldFormSet = formset_factory(AddFormFieldFormx, extra=1)
        formset = fieldFormSet()
        templateForm = AddFormTemplateFormx()

    theContext['fieldNames'] = [i.name for i in FormField._meta.fields[1:-1]]
    theContext["templateform"] = templateForm
    theContext['formset'] = formset
    return render(request, "LearniumApp/formTemplateAdd.html", theContext)


@login_needed
def sendEmailView(request):

    context = {}
    return render(request, "LearniumApp/emailSent.html", context);

@login_needed
def IDView(request, TEMPLATE_ID):

    events = request.user.formtemplate_set.all()
    theContext = {}
    # note that TEMPLATE_ID is a string variable and not an int
    if int(TEMPLATE_ID) <= len(events) and int(TEMPLATE_ID) > 0:

        display = None

        selectedData = events[int(TEMPLATE_ID)-1]
        TemplateFormSet = inlineformset_factory(FormTemplate, FormField, extra=1)
        if request.method == "POST":

            formset = TemplateFormSet(request.POST, instance=selectedData)
            templateForm = AddFormTemplateFormx(request.POST, instance=selectedData)

            if formset.is_valid() and templateForm.is_valid():

                formset.save()
                templateForm.save()
                display = "You have successfully updated the event !"
                #theContext["display"] = display

                return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewID", args=(TEMPLATE_ID,)))
                #return render(request, "LearniumApp/templatesID.html", theContext)

        else:
            templateForm = AddFormTemplateFormx(instance=selectedData)
            formset = TemplateFormSet(instance=selectedData)

    else:
        return HttpResponseNotFound("<h1>Sorry page not found ! </h1>")


    theContext["formset"] = formset
    theContext["templateForm"] = templateForm
    theContext["display"] = display
    theContext["TemplateID"] = TEMPLATE_ID

    return render(request, "LearniumApp/templatesID.html", theContext)


@login_needed
def shareTemplateView(request, TEMPLATE_ID ):

    formtemplates = request.user.formtemplate_set.all()
    hostName = request.META['HTTP_HOST']

    if len(formtemplates) < int(TEMPLATE_ID):
            return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewIndex"))

    if request.method == "POST":
        print request.POST
        recipient = request.POST['emailToSend'].strip().split(" ")

        for i in recipient:
            if validate_email(i) == False:
                theContext = {};
                theContext['templateID'] = TEMPLATE_ID
                theContext['template'] = formtemplates[ int(TEMPLATE_ID) - 1 ]
                theContext['error'] = True
                return render(request, "LearniumApp/sendEmail.html", theContext)

        template = formtemplates[int(TEMPLATE_ID)-1]
        randomString = template.url

        # generating the email.
        htmlContent = '<p>You have been invited for a survey by <b>'+request.user.username+'</b> ! </p><a href="http://'+hostName+'/preview_templates/'+randomString+'">Please click here to answer</a>'
        msg = EmailMultiAlternatives("SimpleSurveyMonkey - invitation for a survey", 'This is the body', 'thisisfrom',bcc=recipient)
        msg.attach_alternative(htmlContent, "text/html")
        msg.send()
        return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewEmailSent"))

    else:
        theContext = {};
        theContext['templateID'] = TEMPLATE_ID
        theContext['template'] = formtemplates[ int(TEMPLATE_ID) - 1 ]

        return render(request, "LearniumApp/sendEmail.html", theContext)

@login_needed
def previewTemplateView(request, TEMPLATE_STRING ):

    theContext = {}
    template = FormTemplate.objects.filter(url = str(TEMPLATE_STRING))
    print len(template), "This is the length of the url string filtered"
    if len(template) != 0:
        template = template[0]
        fields = template.formfield_set.all()

    else:
        return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewIndex"))

    if request.method == "POST":
        tempString = ""
        for i in range(1, len(fields)+1):
            userInput = request.POST.get('item'+str(i), None)

            if userInput:
                tempString += userInput+"\n"


        responseObject = FormResponse(stringResponse=tempString, ownedByWhichTemplate=template)
        responseObject.save()
        return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewThankYou"))

    print template
    if fields[0].fieldChoices == "boolean": boolean = True;
    else: boolean = False;
    theContext['boolean'] = boolean
    theContext['template'] = template
    theContext['fields'] = fields
    theContext['template_string'] = TEMPLATE_STRING
    return render(request, "LearniumApp/previewTemplate.html", theContext)


def thankYouView(request):
    theContext = {}
    return render(request, "LearniumApp/thankYou.html", theContext)

@login_needed
def responseView(request, TEMPLATE_ID):

    theContext = {}
    theContext['templateID'] = TEMPLATE_ID
    templates = request.user.formtemplate_set.all()

    if len(templates) < int(TEMPLATE_ID):
        return HttpResponseRedirect(urlresolvers.reverse("LearniumApp:ViewIndex"))

    template = templates[int(TEMPLATE_ID)-1]

    responses = template.formresponse_set.all()
    responses = [list(enumerate(i.stringResponse.split("\n")[:-1])) for i in responses]

    fields = template.formfield_set.all()
    fieldNames = [i.descriptiveLabel for i in fields]

    responsesFinal = [i[0:min(len(fieldNames), len(i))] for i in responses]
    # collectAll = {}
    # for i in fields:
    #     if i.fieldChoices == "boolean":
    #         collectAll[i.fieldChoices] = 0
    #     else:
    #         collectAll["integer"] = {}
    # print collectAll

    collectall = []
    # numOfResponses = len(responsesFinal)
    #
    # for k in range(len(responsesFinal[0])):
    #     tempList = []
    #     for i in responsesFinal:
    #         tempList.append(i[k][1])
    #     print tempList
    #     numberDict = dict(Counter(tempList))
    #     percentageDict = numberDict.copy()
    #     print numberDict
    #
    #     for i in percentageDict.keys():
    #         percentageDict[i] /= float(numOfResponses)
    #     print "this is final percentageDict", percentageDict
    #     collectall.append(percentageDict)
    # print collectall

    theContext['percentages'] = collectall
    theContext['responses'] = responsesFinal
    theContext['fieldNames'] = fieldNames
    return render(request, "LearniumApp/responses.html", theContext)

