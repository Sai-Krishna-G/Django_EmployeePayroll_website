from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional

    def __str__(self):
        return self.user.username

# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=100,null=False)
    location=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class role(models.Model):
    name=models.CharField(max_length=100,null=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100,null=False)
    last_name = models.CharField(max_length=100)
    salary = models.IntegerField(default=0)
    bonus=models.IntegerField(default=0)
    phone=models.IntegerField(default=0)
    dept = models.ForeignKey(Department,on_delete=models.CASCADE)
    role= models.ForeignKey(role,on_delete=models.CASCADE)
    hire_data=models.DateField()
    hra=models.IntegerField(default=10000)

    def __str__(self):
        return "%s %s %s" %(self.first_name,self.last_name,self.phone)