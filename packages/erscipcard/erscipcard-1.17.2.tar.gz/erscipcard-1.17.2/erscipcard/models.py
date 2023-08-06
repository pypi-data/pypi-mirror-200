from django.db import models
from django.core.exceptions import ValidationError

def valid_date(value):
    val=value.split("/")
    if len(val)==3:
        if int(val[0]) in range(1300,1500):
            if int(val[1]) in range(1,7) and int(val[2]) in range(1,32):
                return value
            if int(val[1]) in range(7,13) and int(val[2]) in range(1,31):
                return value
    raise ValidationError("فرمت تاریخ درست نیست!")

class StateType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class PassType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class User1(models.Model):
	name = models.CharField(max_length=100 ,verbose_name='نام کاربری')
	personeli = models.CharField(max_length=20,unique=True,verbose_name='شماره پرسنلی')
	etebar = models.CharField(max_length=10,validators=[valid_date] ,verbose_name='تاريخ اعتبار')
	pic = models.ImageField(upload_to='images/', blank=True, null=True ,verbose_name='تصویر')
	number = models.IntegerField(default = 1 , unique=True ,verbose_name='شماره کارت')
	def __str__(self):
	    return self.name
		
