from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate,login
from .forms import Company
import openpyxl
from django.http import HttpResponse
from django.template.loader import render_to_string



def index(request):
    return render(request, 'homepage.html')


def user_login(request):
    error = ""
    if request.method == 'POST':
        e = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=e, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'studentlogin.html', locals())

def signup(request):
    error = ""
    if request.method == "POST":
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        idcode = request.POST['idcode']
        email = request.POST['emailid']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username=email, password=password, first_name=fname, last_name=lname)
            UserDetails.objects.create(user=user, idcode=idcode)
            error = "no"
        except:
            error = "yes"
    return render(request, 'studentsignup.html', locals())




def sdash(request):
   if not request.user.is_authenticated:
    return redirect('login')
   notices = Notice.objects.all()
   return render(request,'studentafterlogin.html',{'notices': notices})



def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    userDtls = UserDetails.objects.get(user=user)

    if request.method == "POST":
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        idcode = request.POST['idcode']
        ClgName= request.POST['CollegeName']
        Depart = request.POST['Department']
        ConNo = request.POST['ContactNo']

        SCMarks= request.POST['SSCMarks']
        YPone= request.POST['YOP1']
        
        

        SwD = request.POST['SDip']     
        two = request.POST['YOP2']
        
        BwE= request.POST['BEMarks']
        three= request.POST['YOP3']
        # resumes = request.POST['resumes']
        

        userDtls.user.first_name = fname
        userDtls.user.last_name = lname
        userDtls.idcode = idcode

       
        userDtls.CollegeName = ClgName
        userDtls.Department  = Depart 
        userDtls.ContactNo = ConNo

        userDtls.SSCMarks = SCMarks
        userDtls.YPone = YPone

       
        
        userDtls.SwD = SwD
        userDtls.YOP2 = two

        userDtls.BEMarks  = BwE
        userDtls.YOP3= three
        # userDtls.resumes = resumes
       


        try:
            userDtls.save()
            userDtls.user.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'profile.html', locals())



def jobapplied(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = User.objects.get(id=request.user.id)
    userDtls = UserDetails.objects.get(user=user)
    myapplied_jobs = jobs.objects.filter(user=userDtls)
    myreg_entries = Myreg.objects.filter(companyName__in=[job.companyName for job in myapplied_jobs])
    uploaded_excel_files = UploadedExcel.objects.filter(company__in=myreg_entries)
    
    return render(request, 'jobapplied.html', {'myapplied': myapplied_jobs, 'uploaded_excel_files': uploaded_excel_files})





# def tpopost(request):
#     queryset = Myreg.objects.all()
#     user = User.objects.get(id=request.user.id)
#     userDtls = UserDetails.objects.get(user=user)
#     if request.method == "POST":
#         try:
#             # Fetch companyName from the form data
#             companyName = request.POST.get('companyName')
#             # Create a new 'jobs' object with the companyName and user details
#             jobs.objects.create(user=userDtls, applied="Yes", companyName=companyName)
#             error = "no"
#         except:
#             error = "yes"
#         return redirect('jobapplied')
    
#     return render(request, 'tpopost.html', {'queryset': queryset})

def tpopost(request):
    queryset = Myreg.objects.all()
    user = User.objects.get(id=request.user.id)
    userDtls = UserDetails.objects.get(user=user)
    
    if request.method == "POST":
        try:
            # Fetch companyName from the form data
            companyName = request.POST.get('companyName')
            
            # Check if the user has already applied for this company
            already_applied = jobs.objects.filter(user=userDtls, companyName=companyName).exists()
            if already_applied:
                error = companyName  # Pass company name as error message
            else:
                # Create a new 'jobs' object with the companyName and user details
                jobs.objects.create(user=userDtls, applied="Yes", companyName=companyName)
                error = "no"
        except:
            error = "yes"
        
        if error != "no":
            return render(request, 'tpopost.html', {'queryset': queryset, 'error': error})
        
        return redirect('jobapplied')
    
    return render(request, 'tpopost.html', {'queryset': queryset})





def changePassword(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    # error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'forgot.html', locals())


def tpologin(request):
   return render(request,'tpologin.html')


def tpoafterlogin(request):
   return render(request,'tpoafterlogin.html')

def dash(request):
    return render(request,'tpologin.html')


def reg(request):
    queryset = Myreg.objects.all()
    if request.method == 'POST':
            # Myreg.objects.create(
            #     companyName=request.POST['companyName'],
            #     driveDate=request.POST['driveDate'],
            #     link=request.POST['link'],
            # )
        form = Company(request.POST)
        if form.is_valid():
            form.save()
            queryset = Myreg.objects.all()
            return redirect('register')  # Redirect to a success page
    else:
        form = Company()


    return render(request, 'companyreg.html', {'form': form, 'queryset': queryset})

def delete_drive(request, pk):
    drive = get_object_or_404(Myreg, pk=pk)
    drive.delete()
    return redirect('register')


# def jlist(request):
#     # companies = Myreg.objects.all()
#     if request.method == 'POST':
#         comname = request.POST.get('issue')
#         Notice.objects.create(comname=comname)
#         return redirect('joblist')

#     return render(request, 'tpojoblist.html')

def jlist(request):
    if request.method == 'POST':
        comname = request.POST.get('comname')  # Corrected field name to 'comname'
        rounds = request.POST.get('rounds')    # Retrieve 'rounds' field value
        duration = request.POST.get('duration')  # Retrieve 'duration' field value
        Notice.objects.create(comname=comname, rounds=rounds, duration=duration)
        return redirect('joblist')

    return render(request, 'tpojoblist.html')



# def jround(request):
#     if request.method == 'POST':
#         scheduled_company_name = request.POST.get('companyName', '')
#         scheduled_job_Role = request.POST.get('jobRole', '')
#         scheduled_Package = request.POST.get('Package', '')
#         scheduled_Location = request.POST.get('Location', '')
#         scheduled_JOB_Discription = request.POST.get('JOBDiscription', '')
#         scheduled_drive_round = request.POST.get('round', '')
    
#         request.session['scheduled_company_name'] = scheduled_company_name
#         request.session['scheduled_job_Role'] = scheduled_job_Role
#         request.session['scheduled_Package'] = scheduled_Package
#         request.session['scheduled_Location'] = scheduled_Location
#         request.session['scheduled_JOB_Discription'] = scheduled_JOB_Discription
#         request.session['scheduled_drive_round'] = scheduled_drive_round

#         # Pass the scheduled company details to the student dashboard view
#         return render(request, 'studentafterlogin.html', {
#             'scheduled_company_name': scheduled_company_name,
#             'scheduled_drive_round': scheduled_drive_round,
#             # Pass other scheduled company details as needed
#         })
    
    


# def studapp(request):
#    # Fetch all company names from Myreg model
#     companies = Myreg.objects.values_list('companyName', flat=True)
#     context = {'companies': companies}
#     return render(request, 'tpoappstud.html', context)

def studapp(request):
    if request.method == 'POST':
        for company in Myreg.objects.all():
            excel_file = request.FILES.get('excel_file_' + str(company.id))
            company_id = request.POST.get('company_id_' + str(company.id))
            if excel_file and company_id:
                company = Myreg.objects.get(id=company_id)
                uploaded_excel = UploadedExcel(company=company, excel_file=excel_file)
                uploaded_excel.save()
        return redirect('tpoappstud')
    
    companies = Myreg.objects.all()
    context = {'companies': companies}
    return render(request, 'tpoappstud.html', context)


def stuprofile(request):
    
    user = User.objects.all()
    queryset = UserDetails.objects.all()
    
    return render(request,'studentprofiles.html',{'user':user ,'queryset': queryset})






