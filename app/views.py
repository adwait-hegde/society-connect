from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
# from django.http import HttpResponse
from django.shortcuts import redirect, render
from .tasks import *
from .forms import NoticeBoardForm
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

# send_mail_func.delay()
# return HttpResponse("Sent!")
    # form = NoticeBoardForm()


# Create your views here.
def home(request):
    if request.method=="GET":
        return render(request, 'app/home.html')
    raise Http404('No such request')

@csrf_exempt
def signin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            messages.success(request,"Login Successful! Welcome to your Dashboard...")
            login(request,user)
            print("Login Success!")
            return redirect('/dashboard/')
        else:
            messages.error(request,"Wrong credentials,Please try again !")
            print("Wrong credentials,Please try again !")
            return redirect('/login/')
    if request.method == 'GET':
        return render(request, 'app/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def dashboard(request):
    user = request.user
    notices = NoticeBoard.objects.all()
    notice = notices.last()
    noticecount = notices.count()
    last_notices = notices.filter(date_added__gte=datetime.now() + relativedelta(months = -1)).count()
    new_notices = notices.filter(date_added__gte=datetime.now() + relativedelta(days = -7)).count()
    try:
        sm = SocietyMember.objects.get(user=user)
        print("sm")
        
        if sm.is_owner:
            txns = Transaction.objects.filter(user=sm)[::-1][:6]
            bills = MaintenanceBill.objects.filter(owner=sm).reverse()[::-1][:6]
            commember = CommitteeMember.objects.filter(user=user).count() != 0
            return render(request, 'app/owner2.html', {"sm": sm, 'notice':notice,'txns':txns, 'bills':bills,'noticecount':noticecount, 'last_notices':last_notices, 'new_notices':new_notices, 'commember':commember })
        else:
            return render(request, 'app/tenant.html', {"sm": sm, 'notice':notice, 'noticecount':noticecount, 'last_notices':last_notices, 'new_notices':new_notices })
    except:
        return redirect('/')
        # try:
        #     sm = CommitteeMember.objects.get(user=user)
        #     print("cmmmm")
        # except:
        #     print("watchman")
    # return render(request, 'app/member.html')


@login_required
def memberdash(request):
    try:
        skm = CommitteeMember.objects.get(user=request.user)
    except:
        return redirect('/dashboard/')

        
    smem = SocietyMember.objects.filter(is_owner=True, user__is_active=True)
    
    if request.method=="POST":
        # print(request)
        userid = request.POST.get('userselect')
        mode = request.POST.get('gridRadios')
        details = request.POST.get('details')
        money = float(request.POST.get('money'))
        success = request.POST.get('success')=='on'
        # print(userid, mode,details,money,success)
        sm = SocietyMember.objects.get(pk=userid)
        # print()
        # print(money,detail)
        txn = Transaction(user=sm, amount=money, status=success, mode=mode, detail=details)
        tid = txn.make_transaction()
        if txn.status:
            sm.dues -= money
            sm.save()
        send_mail_txn_status.delay(tid, sm.user.pk)

    return render(request, 'app/member.html', {'smem':smem})
    


@login_required
def paymentgateway(request):
    # if request.method == "POST":
    #     sm = SocietyMember.objects.get(user=request.user)
    #     amount = int(sm.get_dues()*100)
    #     client = razorpay.Client(auth=("rzp_test_s5q0CFlRW6xIZg", "lb2dLjsTT4RVJBlSdQJXhKyq"))
    #     payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    #     print(payment)

    if request.method == "GET":
        try:
            sm = SocietyMember.objects.get(user=request.user)
            if sm.get_dues()==0:
                return redirect('/dashboard/')
            if sm.is_owner:
                # print(sm.get_dues())
                return render(request, 'app/payment.html', {"duers":sm.get_dues(), "dueps":int(sm.get_dues()*100)})
            else:
                return redirect('/dashboard/')
        except:
            return redirect('/dashboard/')

    return render(request, 'app/payment.html')


@csrf_exempt
def success(request):
    if request.method == "POST":
        print(request.POST)
        money = request.POST.get('money')
        detail = request.POST.get('razorpay_payment_id')
        sm = SocietyMember.objects.get(user=request.user)
        print()
        print(money,detail)
        txn = Transaction(user=sm, amount=money, status=True, mode='ONLINE', detail=detail)
        tid = txn.make_transaction()
        sm.dues = 0
        sm.save()
        send_mail_txn_status.delay(tid, request.user.pk)
        # return redirect('/success')
        return render(request, "app/success.html")
    return redirect('/paymentgateway/')
#  'name': ['test'], 
# 'razorpay_payment_id': ['pay_INxGKZnGeogOgt'], 
# 'org_logo': [''], 'org_name': ['Razorpay Software Private Ltd'], 'checkout_logo': ['https://cdn.razorpay.com/logo.png'], 'custom_branding': ['false']}


@login_required
def transactions(request):
    if request.method == "GET":
        try:
            sm = SocietyMember.objects.get(user=request.user)
            if sm.is_owner:
                txns = Transaction.objects.filter(user=sm)[::-1]
                return render(request, 'app/transactions.html', {"txns":txns})
            else:
                return redirect('/dashboard/')
        except:
            return redirect('/dashboard/')


@login_required
def addnotice(request):
    if request.method == "POST":
        try:
            cm = CommitteeMember.objects.get(user=request.user)
        except:
            return redirect("/dashboard/")

        form = NoticeBoardForm(request.POST)
        if form.is_valid():
            notice = form.cleaned_data['notice']
            print(notice)
            noticebrd = NoticeBoard(added_by=cm, notice=notice, date_added=datetime.now())
            noticebrd.save()
            
            notibrd = NoticeBoard.objects.all().last()
            send_mail_notice.delay(notibrd.pk)
            # send_mail_notice.delay(notice)
            # send_mail_func.delay()
            # SEND EMAIL send_mail_func.delay()
            # print(" Bill ceated for: ",sm)
            # send_mail_func.delay()
            return redirect('/dashboard/')

    if request.method == "GET":
        try:
            sm = CommitteeMember.objects.get(user=request.user)
        except:
            return redirect("/dashboard/")
        # smem = SocietyMember.objects.filter(is_owner=True, user__is_active=True)
        form = NoticeBoardForm()
        return render(request, 'app/addnotice.html', {'form':form})



@login_required
def notice(request):
    if request.method == "GET":
        notices = NoticeBoard.objects.all().order_by("date_added").reverse()
        return render(request, 'app/notice.html', {'notices':notices})


@login_required
def notice_one(request, pk):
    if request.method == "GET":
        notice = NoticeBoard.objects.get(pk=pk)
        return render(request, 'app/noticesingle.html', {'notice':notice})

# @login_required
def addbill(request):
    if request.method == "POST":
        try:
            sm = CommitteeMember.objects.get(user=request.user)
        except:
            return redirect("/dashboard/")
    
        billdet = request.POST.get('billdet')
        details = json.loads(billdet)
        smem = SocietyMember.objects.filter(is_owner=True, user__is_active=True)
        total = 0
        for sm in smem:
            bill = MaintenanceBill(owner=sm)
            bill.save()
            for detail in details['det']:
                if sm.id in detail['id']:
                    newdet = BillDetail(bill=bill, description=detail['desc'], amount=detail['amt'])
                    total += float(detail['amt'])
                    newdet.save()
            if sm.get_dues()>10:
                newdet = BillDetail(bill=bill, description="21% Interest on previous dues", amount=sm.get_dues()*21/100)
                total+=(sm.get_dues()*21/100)
                newdet.save()
            bill.total = total
            sm.dues += total
            sm.save()
            bill.save()
            # send_mail_func.delay()
            # SEND EMAIL send_mail_func.delay()
            # print(" Bill ceated for: ",sm)
            send_mail_func.delay()
            return redirect('/dashboard/')

    if request.method == "GET":
        try:
            cm = CommitteeMember.objects.get(user=request.user)
        except:
            return redirect("/dashboard/")
        smem = SocietyMember.objects.filter(is_owner=True, user__is_active=True)
        return render(request, 'app/addbilldetail.html', {'sm':smem})





            
@login_required
def maintenancebill (request):
    if request.method == "GET":
        try:
            sm = SocietyMember.objects.get(user=request.user)
            if sm.is_owner:
                bills = MaintenanceBill.objects.filter(owner=sm)
                return render(request, 'app/maintenancebill.html', {"bills":bills})
            else:
                return redirect('/dashboard/')
        except:
            return redirect('/dashboard/')
            
@login_required
def maintenancebill_one(request, pk):
    if request.method == "GET":
        try:
            sm = SocietyMember.objects.get(user=request.user)
            if sm.is_owner:
                bill = MaintenanceBill.objects.get(pk=pk)
                
                # print("BILLL: "+bill)
                dets = BillDetail.objects.filter(bill=bill)
                
                return render(request, 'app/maintenancebillsingle.html', {"bill":bill, "dets":dets})
            else:
                return redirect('/dashboard/')
        except:
            return redirect('/dashboard/')








# djrs
# celery -A societyconnect.celery worker --pool=solo -l info
# celery -A societyconnect beat -l info
# pip freeze > requirements.txt