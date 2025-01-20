from django.db import models                                                                        
from django.contrib.auth.models import User
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    idcode = models.CharField(max_length=12, null=True)

    dob = models.DateField(null=True)
    CollegeName = models.CharField(max_length=250, null=True)
    Department = models.CharField(max_length=50, null=True)
    ContactNo = models.CharField(max_length=12, null=True)
    SSCMarks = models.FloatField(max_length=10, null=True)
    YPone = models.CharField(max_length=5, null=True)
    SwD = models.FloatField(max_length=10, null=True)
    YOP2 = models.CharField(max_length=5, null=True)
    BEMarks = models.FloatField(max_length=10, null=True)
    YOP3 = models.CharField(max_length=5, null=True)
    # resumes = models.FileField(upload_to= 'resumes/')
    

def __str__(self):
        return self.user.first_name


#tpo
class Myreg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    companyName = models.CharField(max_length=100)
    driveDate = models.DateField(null=True)
    link = models.URLField()
    jobRole = models.CharField(max_length=100,null=True)
    package = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=100,null=True)
    jobDescription = models.TextField(max_length=1000,null=True)

    def __str__(self):
        return "%s" %(self.companyName)
   
    class Meta:
        db_table="placement"

class jobs(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True)
    applied = models.CharField(max_length=150, null=True)
    companyName = models.CharField(max_length=100, null=True)    
    def __str__(self):
        return "%s" %(self.applied)
    


class UploadedExcel(models.Model):
    company = models.ForeignKey(Myreg, on_delete=models.CASCADE, related_name='uploaded_files',null=True)
    excel_file = models.FileField(upload_to='uploads/', blank=True)


class Notice(models.Model):
    comname = models.TextField(null=True)
    rounds = models.TextField(null=True)
    duration = models.TimeField(null=True)
    created_at = models.DateField(auto_now_add=True,null=True)


    def __str__(self):
        return self.comname