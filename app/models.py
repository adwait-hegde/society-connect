from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from ckeditor.fields import RichTextField

# Create your models here.

# class Book(models.Model):
#     title = models.CharField(max_length=100)

#     @classmethod
#     def create(cls, title):
#         book = cls(title=title)
#         # do something with the book
#         return book

# book = Book.create("Pride and Prejudice")

class SocietyMember(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    is_owner = models.BooleanField(default=None)
    room_no = models.IntegerField()
    phone_no = models.FloatField()
    dues = models.FloatField()

    def __str__(self):
        if self.is_owner:
            return str(self.user.username) + " " + str(self.room_no) +" owner" 
        else:
            return str(self.user.username) + " " + str(self.room_no) +" tenant" 

    def edit_phone_no(self,phone_no):
        self.phone_no = phone_no
        try:
            self.save()
            return "Successful"
        except Exception as e:
            return e

    def get_dues(self):
        return self.dues

    def get_dues_rs(self):
        return int(self.dues)

    def get_dues_ps(self):
        return int((self.dues - int(self.dues))*100)


ROLE_CHOICES = (
    ('SEC', 'Secretary'),
    ('CP', 'Chairperson'),
    ('TR', 'Treasurer'),
    ('SC', 'Sub Committee'),
    ('EM', 'Ex-Member'),
)

class CommitteeMember(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    role = models.CharField(max_length=3, choices=ROLE_CHOICES)

    def __str__(self):
        return str(self.user.username) + " " + str(self.role)

    def is_committee_member(self):
        if self.role in ['SEC', 'CP', 'TR']:
            return True
        return False


class Watchman(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    salary = models.IntegerField()
    phone_no = models.FloatField()

    def edit_phone_no(self,phone_no):
        self.phone_no = phone_no
        try:
            self.save()
            return "Successful"
        except Exception as e:
            return e

    def edit_salary(self,salary):
        self.salary = salary
        try:
            self.save()
            return "Successful"
        except Exception as e:
            return e


class MaintenanceBill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(SocietyMember,on_delete=models.SET_NULL,null=True)
    total = models.FloatField(default=0)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.bill_id) + " " + str(self.date) + " " + str(self.owner)


    def get_total(self):
        return self.total

    # def remove_billdetail(self,)



class BillDetail(models.Model):
    bill = models.ForeignKey(MaintenanceBill,on_delete=models.CASCADE)
    description = models.CharField(max_length=30)
    amount = models.FloatField()

    def edit_desc(self,desc):
        self.description = desc
        try:
            self.save()
            return "Successful"
        except Exception as e:
            return e
        
    def edit_amount(self,amount):
        self.amount = amount
        try:
            self.save()
            return "Successful"
        except Exception as e:
            return e
        

class Transaction(models.Model):
    TNX_CHOICES = (
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('ONLINE', 'Online - Razor Pay'),
    )
    tid = models.AutoField(primary_key=True)
    user = models.ForeignKey(SocietyMember,on_delete=models.SET_NULL,null=True)
    amount = models.FloatField()
    status = models.BooleanField()
    mode = models.CharField(max_length=6, choices=TNX_CHOICES)
    detail = models.CharField(max_length=25)
    date = models.DateTimeField(auto_now=True)

    def make_transaction(self):
        self.save()


class NoticeBoard(models.Model):
    added_by = models.ForeignKey(CommitteeMember, on_delete=models.SET_NULL,null=True)
    date_added = models.DateTimeField(auto_now=True)
    last_edited = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    notice = RichTextField(blank=True, null=True)

'''
class OninePoll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    poll_details = models.CharField(max_length=50)
    creator = models.ForeignKey(CommitteeMember, on_delete=models.SET_NULL,null=True)
    date_added = models.DateTimeField(auto_now=True)
    valid_till = models.DateTimeField()


class PollOption(models.Model):
    poll = models.ForeignKey(OninePoll, on_delete=models.CASCADE)
    option = models.CharField(max_length=50)


class PollResponse(models.Model):
    user = models.ForeignKey(SocietyMember, on_delete=models.SET_NULL,null=True)
    response = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    poll = models.ForeignKey(OninePoll, on_delete=models.CASCADE)


class Complaint(models.Model):
    COMPLAINT_STATUS = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
    )
    cid = models.AutoField(primary_key=True)
    user = models.ForeignKey(SocietyMember, on_delete=models.SET_NULL,null=True)
    complaint_title = models.CharField(max_length=20)
    complaint = models.CharField(max_length=150)
    status = models.CharField(max_length=6, choices=COMPLAINT_STATUS)


class ComplaintRemark(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    complaint_remark = models.CharField(max_length=150)
    status = models.CharField(max_length=6, choices=COMPLAINT_STATUS)
'''