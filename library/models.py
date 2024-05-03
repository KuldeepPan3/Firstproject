from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Student(models.Model):
   name=models.CharField(max_length=55,blank=False,null=False)
   email=models.EmailField()
   age=models.IntegerField()
   gender=models.CharField(max_length=55,blank=False,null=False)

   def __str__(self):
      return self.name
   
class Books(models.Model):
   bid=models.IntegerField(primary_key=True)
   btitle = models.CharField(max_length=150)
   bauthor = models.CharField(max_length=200)


   def __str__(self):
      return self.btitle
   
class IssuedItem(models.Model):
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField(default=date.today(),blank=False)
    return_date = models.DateField(blank=True,null=True)

    # property to get book name
    @property
    def book_name(self):
        return self.book_id.btitle
    
    # property to get author name
    @property
    def username(self):
        return self.user_id.username
    
    def __str__(self):
        return self.book_id.btitle + ' issued by ' + self.user_id.first_name + ' on ' + str(self.issue_date)   