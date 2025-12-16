from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import  (
    Lokko_uddessho,About,Leftside,Gallery_Top, 
    Head_Teachers_speach, Notice_board, Result,  News_headline, Montri, 
    Sochib, DG_or_Chairman, Upo_Montri, SineBoard, Students_Information,
    Teachers_Information, Other_Employee_Information, Gallery, 
    Cultural_Program, Sports, Web_Heading, ImportantLink
)
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, View
)
from students.models.class_studn import ClassName, ClassYear, SectionClas
from .forms import OnlineAdmissionForm, complainform
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from students.models import StudentsInfo


def home(request):
    return render(request, 'institute/homepage.html')


def all_global_context(request):
    site_headline = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    education_minister = Montri.objects.last()
    sub_education_minister = Upo_Montri.objects.last()
    secretory = Sochib.objects.last()
    director_general = DG_or_Chairman.objects.last()
    gallery = Gallery.objects.order_by('id').reverse()[:10]
    #For notice board
    notice = Notice_board.objects.order_by('id').reverse()[:5]
    gallery_slider_top = Gallery_Top.objects.order_by('id').reverse()[:2]
    leftsideqt = Leftside.objects.last()
    sinebord = SineBoard.objects.last()
    important_link = ImportantLink.objects.order_by('id').reverse()[:5]
    students = StudentsInfo.objects.filter(unique_roll=str(request.user)).last()
    user_info = request.user
    context = {
        'sinebord':sinebord,
        'qt':leftsideqt,
        'gallery':gallery,
        'gallerytp':gallery_slider_top,
        'notice': notice,
        'marq': marquee_notice,
        'webname': site_headline,
        'montri': education_minister,
        'upomontri': sub_education_minister,
        'sochib': secretory,
        'dg': director_general,
        'important_link': important_link,
        'user': user_info,
        'students': students,
    }
    return context


    #for notice board page all notice
def notice_board(request):
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    montri = Montri.objects.last()
    upomontri = Upo_Montri.objects.last()
    sochib = Sochib.objects.last()
    dg = DG_or_Chairman.objects.last()
    gallery = Gallery.objects.order_by('id').reverse()[:10]
    #all notice
    noticeboard = Notice_board.objects.all()
    halnagad_date = Notice_board.objects.last()
    allnotice = Notice_board.objects.order_by('-id').all()
    if request.method == 'GET':
        showing_result_number = request.GET.get('result')
        if showing_result_number!= None:    
            paging = Paginator(allnotice, showing_result_number)
            page_nub = request.GET.get('page')
            page_obj = paging.get_page(page_nub)
        else:
            paging = Paginator(allnotice, 5)
            page_nub = request.GET.get('page')
            page_obj = paging.get_page(page_nub)
    #searching start
    searchinfo = None
    if request.method == 'GET':
        st = request.GET.get('notice_search')
        if st!= None:
            searchinfo = Notice_board.objects.filter(title__icontains=st)   
    #searching ends
    return render(
        request, 'institute/noticeboard_page.html',
        {'gallery':gallery,
         'marq': marquee_notice,
         'search':searchinfo, 
         'up_date': halnagad_date, 
         'all_notice': noticeboard, 
         'webname': webheading, 
         'montri': montri, 
         'upomontri': upomontri, 
         'sochib': sochib, 
         'dg': dg, 
         'notice': page_obj})




class StudentsInfoView(View):
    def get(self, request):
        class_nm = ClassName.objects.all()
        session = ClassYear.objects.all()

        context = {
            'classes': class_nm,
            'session': session,
        }
        return render(request, 'institute/students_info.html', context)

    def post(self, request):
        stdn_info = None
        stdn_info_search = None
        
        class_name = request.POST.get('class_nm')
        session = request.POST.get('session')

        session_ins = ClassYear.objects.filter(id=session).last()
        class_nm_ins = ClassName.objects.filter(id=class_name).last()
        print(session_ins, class_nm_ins, 'works')

        
        if class_name and session:
            stdn_info = StudentsInfo.objects.filter(
                class_name=class_nm_ins,
                class_name__class_nm = session_ins,
            )
            # print(stdn_info, 'works')

        search = request.POST.get('students_search3')
        if search:
            stdn_info_search = StudentsInfo.objects.filter(
                Q(name__icontains=search) | Q(unique_roll__icontains=search)
            )

        # Context for rendering
        context = {
            'student_info': stdn_info,
            'search': stdn_info_search,
            'classes': ClassName.objects.all(),  # Fetch classes again for context
            'session': ClassYear.objects.all(),   # Fetch sessions again for context
        }
        return render(request, 'institute/students_info.html', context)



#Students Information
# def students_info(request):
#     stdn_info = None
#     stdn_info_search = None
    
#     if request.method == 'POST':
#         class_name = request.POST.get('class_nm')
#         session = request.POST.get('session')
#         session_ins = ClassYear.objects.filter(id=session).last()
#         class_nm_ins = ClassName.objects.filter(id=class_name).last()
#         # Assuming 'class_nm' and 'session' correspond to IDs in your database
#         if class_name and session:
#             stdn_info = StudentsInfo.objects.filter(
#                 class_name = class_nm_ins,
#                 session= session_ins,
#                 # Q(class_name_id=class_name) & Q(session_id=session)
#             )

#         ss = request.POST.get('students_search3')
#         if ss:
#             stdn_info_search = StudentsInfo.objects.filter(
#                 Q(name__icontains=ss) | Q(unique_roll__icontains=ss)
#             )
    
#     elif request.method == 'GET':
#         session = ClassYear.objects.all()
#         class_nm = ClassName.objects.all()

#         context = {
#             'classes': class_nm,
#             'session': session,
#         }

#     # Context for rendering
#     context = {
#         'student_info': stdn_info,
#         'search': stdn_info_search,
#         'classes': class_nm,
#         'session': session,
#     }
#     return render(request, 'institute/students_info.html', context)

    # stdn_info = None
    # st = None
    # if request.method == 'POST':
    #     class_name = request.POST.get('class_nm')
    #     session = request.POST.get('session')
    #     if st and sa!= None:
    #         stdn_info = StudentsInfo.objects.filter(
    #             Q(class_name__icontains=st) & Q(class_name__class_nm__icontains=sa))
    # stdn_info_search = None
    # if request.method == 'POST':
    #     ss = request.POST.get('students_search3')
    #     if ss!= None:
    #         stdn_info_search = StudentsInfo.objects.filter(
    #             Q(name__icontains=ss) | Q(unique_roll__icontains=ss))  
    # # webheading = Web_Heading.objects.last()
    # # marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    # context = {'student_info':stdn_info, 
    #            'st':st, 
    #            'search':stdn_info_search, 
    #         #    'webname':webheading, 'marq':marquee_notice 
    #              }
    # return render(request, 'institute/students_info.html', context, )


def students_details(request, id):
    if request.method == 'GET':
        pi = StudentsInfo.objects.get(pk=id)
    else:
        pi = StudentsInfo.objects.get(pk=id)
    # webheading = Web_Heading.objects.last()
    # marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(
            request, 'institute/students_database.html', 
            {
                'stinfo': pi, 
                # 'webname':webheading,
                # 'marq':marquee_notice
            }
        )


#result showing
def result(request):
    stdn_info = None
    # st = None
    if request.method == 'POST':
        s1 = request.POST.get('result3')
        s2 = request.POST.get('result4')
        s3 = request.POST.get('result5')
        s4 = request.POST.get('result6')
        s5 = request.POST.get('result7')
        if s1 and s2 and s3 and s4 and s5!= None:
            stdn_info = Result.objects.filter(
                Q(class_name__icontains=s1) 
                & Q(session__icontains=s2) 
                & Q(exam_year__icontains=s3) 
                & Q(exam_type__icontains=s4)  
                & Q(unique_roll__icontains=s5)
                )
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request, 'institute/result.html',
                   {
                        'marq': marquee_notice,
                        'webname': webheading,
                        'result':stdn_info
                    }
                )


class OnlineAdmissionView(View):
    def get(self, request, *args, **kwargs):
        onlineadm = OnlineAdmissionForm()
        webheading = Web_Heading.objects.last()
        marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
        return render(request, 'institute/onlineadmission.html', {
            'marq': marquee_notice,
            'webname': webheading,
            'fm': onlineadm
        })

    def post(self, request, *args, **kwargs):
        onlineadm = OnlineAdmissionForm(request.POST, request.FILES)
        if onlineadm.is_valid():
            form = onlineadm.save(commit=False)
            name = form.student_name_en
            amount = form.admission_fee
            form.save()
            messages.success(request, 'আবেদনটি সফলভাবে সম্পন্ন হয়েছে, ধন্যবাদ!!')
            return redirect(sslcommerz_payment_gateway(request, name, amount))
            # return redirect('some_view_name')  # Replace with your desired redirect view
        else:
            webheading = Web_Heading.objects.last()
            marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
            return render(request, 'institute/onlineadmission.html', {
                'marq': marquee_notice,
                'webname': webheading,
                'fm': onlineadm
            })


# def OnlineAddmission(request):
#     if request.method == 'POST':
#        onlineadm = OnlineAdmissionForm(request.POST, request.FILES) 
#        if onlineadm.is_valid():
#         messages.success(request, 'আবেদনটি সফলভাবে সম্পন্ন হয়েছে, ধন্যবাদ!!')
#         onlineadm.save()
#     else:
#         onlineadm = OnlineAdmissionForm()
#     webheading = Web_Heading.objects.last()
#     marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
#     return render(request, 'institute/onlineadmission.html', 
#                   {'marq': marquee_notice,
#                    'webname': webheading,
#                    'fm': onlineadm})


def complain(request):
    if request.method == 'POST':
       comp = complainform(request.POST) 
       if comp.is_valid():
        messages.success(request, 'আপনার পরামর্শ বা অভিযোগটি সফলভাবে সাবমিট হয়েছে, ধন্যবাদ!!')
        comp.save()
    else:    
        comp = complainform()
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request, 'institute/complain.html',
                   {'marq': marquee_notice,
                    'webname': webheading,
                    'com':comp})


def contact_page(request):
    # webheading = Web_Heading.objects.last()
    # marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request, 'institute/contact.html',)


def gallery_page(request):
    gallery = Gallery.objects.all()
    paging = Paginator(gallery, 3)
    page_nub = request.GET.get('page')
    page_obj = paging.get_page(page_nub)
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request, 'institute/gallery.html',
                  {'notice': page_obj,
                   'marq': marquee_notice,
                   'webname': webheading,
                   'g':gallery})


def teachers_page(request):
    teacher = Teachers_Information.objects.all()
    paging = Paginator(teacher, 10)
    page_nub = request.GET.get('page')
    page_obj = paging.get_page(page_nub)
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request, 'institute/teacher_info.html',
                  {'notice': page_obj,
                   'marq': marquee_notice,
                   'webname': webheading,})


def stafs_page(request):
    staf = Other_Employee_Information.objects.all()
    paging = Paginator(staf, 10)
    page_nub = request.GET.get('page')
    page_obj = paging.get_page(page_nub)
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request, 'institute/staf.html',
                  {'notice': page_obj,
                   'marq': marquee_notice,
                   'webname': webheading,})


def cultur(request):
    cultur= Cultural_Program.objects.all()
    paging = Paginator(cultur, 3)
    page_nub = request.GET.get('page')
    page_obj = paging.get_page(page_nub)
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request, 'institute/cultural.html',
                  {'notice': page_obj,
                   'marq': marquee_notice,
                   'webname': webheading,})


def sports(request):
    sports= Sports.objects.all()
    paging = Paginator(sports, 3)
    page_nub = request.GET.get('page')
    page_obj = paging.get_page(page_nub)
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request, 'institute/sports.html',
                  {'notice': page_obj,
                   'marq': marquee_notice,
                   'webname': webheading,})


def clg_history(request):
    about = About.objects.last()
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request,'institute/history.html', 
                  {'about': about, 
                   'marq': marquee_notice, 
                   'webname': webheading,} )


def speach(request):
    speach = Head_Teachers_speach.objects.last()
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request,'institute/speach.html',
                   {'speach': speach, 
                    'marq': marquee_notice, 
                    'webname': webheading,} )


def lokkouddessho(request):
    lokko = Lokko_uddessho.objects.last()
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    return render(request,'institute/lokko.html', 
                  {'lokko': lokko, 
                   'marq': marquee_notice,
                    'webname': webheading,} )


def newspage(request):
    webheading = Web_Heading.objects.last()
    marquee_notice = News_headline.objects.order_by('id').reverse()[:3]
    montri = Montri.objects.last()
    upomontri = Upo_Montri.objects.last()
    sochib = Sochib.objects.last()
    dg = DG_or_Chairman.objects.last()
    gallery = Gallery.objects.order_by('id').reverse()[:10]
    #all notice
    noticeboard = Notice_board.objects.all()
    halnagad_date = Notice_board.objects.last()
    allnotice = News_headline.objects.order_by('-id').all()
    if request.method == 'GET':
        showing_result_number = request.GET.get('result')
        if showing_result_number!= None:    
            paging = Paginator(allnotice, showing_result_number)
            page_nub = request.GET.get('page')
            page_obj = paging.get_page(page_nub)
        else:
            paging = Paginator(allnotice, 5)
            page_nub = request.GET.get('page')
            page_obj = paging.get_page(page_nub)
    #searching start
    searchinfo = None
    if request.method == 'GET':
        st = request.GET.get('notice_search')
        if st!= None:
            searchinfo = News_headline.objects.filter(title__icontains=st)   
    #searching ends
    return render(
        request, 'institute/news.html', 
            {
                'gallery':gallery,
                'marq': marquee_notice,
                'search':searchinfo, 
                'up_date': halnagad_date, 
                'all_notice': noticeboard, 
                'webname': webheading, 
                'montri': montri, 
                'upomontri': upomontri, 
                'sochib': sochib, 
                'dg': dg, 
                'notice': page_obj
            }
            )


# ssl commerz payment gateway

import string
import random
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
from .models import PaymentGateway


def generator_trangection_id(size=7, chars=string.ascii_uppercase + string.digits):
    # Generate a random string of the specified size
    random_part = "".join(random.choice(chars) for _ in range(size))
    # Combine the real transaction ID with the random part
    transaction_id = f"TRX{random_part}"
    return transaction_id


    

def sslcommerz_payment_gateway(
        request,
        name,
        amount
    ):
 
    gateway = PaymentGateway.objects.all().first()
    cradentials = {'store_id': gateway.store_id,
            'store_pass': gateway.store_pass, 'issandbox': True} 
            
    sslcommez = SSLCOMMERZ(cradentials)
    body = {}
    body['total_amount'] = amount
    body['currency'] = "BDT"
    body['tran_id'] = generator_trangection_id()
    body['success_url'] = 'http://localhost:8000/payment/success/'
    body['fail_url'] = 'http://localhost:8000/payment/payment/faild/'
    body['cancel_url'] = 'http://localhost:8000/payment'
    body['emi_option'] = 0
    body['cus_name'] = name
    body['cus_email'] = 'request.data["email"]'
    body['cus_phone'] = 'request.data["phone"]'
    body['cus_add1'] = 'request.data["address"]'
    body['cus_city'] = 'request.data["address"]'
    body['cus_country'] = 'Bangladesh'
    body['shipping_method'] = "NO"
    body['multi_card_name'] = ""
    body['num_of_item'] = 1
    body['product_name'] = "Test"
    body['product_category'] = "Test Category"
    body['product_profile'] = "general"
    body['value_a'] = name

    response = sslcommez.createSession(body)
    return 'https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"]

