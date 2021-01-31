# Create your views here.
#def first_view(request):
#  return render(request,'FaceDetection/first_view.html',{})
import re

from django.conf import settings
from .forms import ImageUploadForm
from .models import basket
from .opencv_dface import opencv_ocr
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password#비밀번호 암호와, 패스워드 체크(db에 있는 거와 일치성 확인)
from .models import User, memo
from django.contrib import messages

#추출 텍스트 전처리
def cleanText(ocrResult):
    pattern= '[a-zA-Z]'
    ocrResult = re.sub(pattern=pattern, repl='', string=ocrResult) #영어대소문자 제거
    pattern = '[^\w\s\.]'   
    ocrResult = re.sub(pattern=pattern, repl='', string=ocrResult) #특수문자 제거(.제외)
    ocrResult=re.sub(' ','',ocrResult)
    ocrResult=ocrResult.rstrip()
    print(ocrResult)
    return ocrResult


#전처리된 텍스트를 리스트로 변경
def strTolist(cleanResult):
    textlist=cleanResult.splitlines()
    textlist= ' '.join(textlist).split()
    return textlist

#가격 내에 .들어있으면 1순위로 pdprice, .안들어있으면 리스트 맨 뒤 값이 pdprice
def choose_pdprice(textlist):
    choose=re.compile('(.)*$')
    if choose.match(textlist):
        return textlist[1]
    else:
        textlist[-1]

#가격 구분점 . 제거
def strToNum(text):
    text = text.replace('.','')
    text = int(text)
    return text


def ocr(request):
    todo_id=request.GET.get('todo_id')    
    uemail=request.session.get('uemail')

    if request.method =='POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            imageURL = settings.MEDIA_URL + form.instance.document.name
            ocrResult = opencv_ocr(settings.MEDIA_ROOT_URL + imageURL)
            print(ocrResult)
            # 추출 텍스트 전처리
            cleanResult=cleanText(ocrResult)
            print('cleanResult:',cleanResult)
            # int, str 조건 설정
            #cleanResult=int_limit(cleanResult)
            #cleanResult=str_limit(cleanResult)
            # 전처리 텍스트 리스트화
            textlist=strTolist(cleanResult)
            print('textlist',textlist)
            # textlist=int_limit(textlist)
            # print('int_limit:',textlist)

            # 제품명, 가격 추출
            pdname=textlist[0]
            # pdprice=strToNum(textlist[1]) #-1
            pdprice=textlist[-1]
            if len(pdprice)>7:
                pdprice=textlist[-2]
            #strToTxt('20201029', ocrResult) #save_to_file
            print(pdname, pdprice)


            return render(request, 'FaceDetection/ocr.html',{'form':form,'uemail':uemail, 'post':post,'cleanResult':cleanResult, 'pdname':pdname, 'pdprice':pdprice,'todo_id':todo_id}) #'ocrResult':ocrResult,
    else:
        print('-----', request.GET.get('pdname'),request.GET.get('pdprice'))
        form = ImageUploadForm()
    return render(request, 'FaceDetection/ocr.html',{'form':form, 'todo_id':todo_id,'uemail':uemail})

def add_item(request):
    if request.method=='POST':

        # 1.  입력값을 확인한다
        pdname=request.POST.get('pdname')
        pdprice=request.POST.get('pdprice')
        pdprice=strToNum(pdprice)
        todo_id=request.POST.get('todo_id')
        # 2. 입력값을 저장한다
        bask=basket(pdname=pdname, pdprice=pdprice, todo_id=todo_id) #pdqty
        bask.save()

    return basketlist(request)

def get_total_price(self): #장본 항목 수량*가격 총 계산
    return sum(basket['pdqty']*basket['pdprice'] for basket in self.values())

def basketlist(request):
    uemail=request.session.get('uemail')
    #basket = basket.objects.all()
    # 3. 장바구니 리스트를 보여준다
    # 3.1 DB에 있는 장바구니 리스트를 호출 - select
    #3.2 form에 담아서 전달한다
    if request.method=='POST':
        todo_id=request.POST.get('todo_id')
    else:
        todo_id=request.GET.get('todo_id')

    #memolist 정보 가져오기
    memoset=memo.objects.all()
    memo_item=memoset.get(id=todo_id)
    mdetail = memo_item.mdetail
    mdetail = mdetail.split('\r\n')
    budget=memo_item.budget
    print('memo_item:',memo_item.mname)


    queryset =basket.objects.all()
    #bask_list=queryset .filter(todo_id=todo_id, done=0) #done=0 : 장볼 항목
    done_list=queryset .filter(todo_id=todo_id) #done=1 : 장본 항목
    print('basketlist todo_id : ', todo_id)
    total=get_total_price(done_list)
    

    context={'done_list':done_list,'total':total, 'todo_id':todo_id, 'mdetail':mdetail, 'memo_item':memo_item,
        "uemail":request.session.get('uemail')}
    
    if total > budget:
        # messages.info(request, '예산을 초과하였습니다!')
        messages.add_message(request,messages.INFO,'예산을 초과하였습니다!')
     
    return render(request, 'FaceDetection/basketlist.html', context)
       
     

def delete_item(request):
    bsno=request.GET.get('bsno')
    item=basket.objects.get(bsno=bsno)
    item.delete()   

    return redirect('/basketlist?todo_id='+request.GET.get('todo_id'))    


def view_item(request):
    uemail=request.session.get('uemail')
    bsno=request.GET.get('bsno')
    item=basket.objects.get(bsno=bsno)
    
    context={'item':item, 'uemail':uemail}
    return render(request, 'FaceDetection/view_item.html', context)

def edit_item(request):
    uemail=request.session.get('uemail')
    bsno=request.GET.get('bsno')
    item=basket.objects.get(bsno=bsno)

    context={'item':item, 'uemail':uemail}
    return render(request, 'FaceDetection/edit_item.html', context)

def update_item(request):
    uemail=request.session.get('uemail')

    if request.method=='POST':
        bsno=request.POST.get('bsno')
        item=basket.objects.get(bsno=bsno)        
        item.pdname=request.POST.get('pdname')
        item.pdprice=request.POST.get('pdprice')
        item.pdqty=request.POST.get('pdqty')
        # 2. 입력값을 저장한다
        item.save()
        print('1111111111111')

   
        item=basket.objects.get(bsno=bsno)
        context={'item':item, 'uemail':uemail}
    return render(request, 'FaceDetection/view_item.html', context)

def update_memo(request):
    uemail=request.session.get('uemail')

    if request.method=='POST':
        id=request.POST.get('id')
        edit_memo=memo.objects.get(id=id)
        edit_memo.mname=request.POST.get('mname')      
        edit_memo.mdetail=request.POST.get('mdetail')
        edit_memo.budget=request.POST.get('budget')
        edit_memo.label=request.POST.get('label')
        # 2. 입력값을 저장한다
        edit_memo.save()
        print('1111111111111')

   
    edit_memo=memo.objects.get(id=id)
    context={'edit_memo':edit_memo, 'uemail':uemail}
    return render(request, 'FaceDetection/edit_memo.html', context)


def signup(request):   #회원가입 페이지를 보여주기 위한 함수
    res_data = {} 
    if request.method == "GET":
        return render(request, 'FaceDetection/signup.html')

    elif request.method == "POST":
        username = request.POST.get('uemail',None)   #딕셔너리형태 (오류남.)
        password = request.POST.get('upw',None)
        re_password = request.POST.get('upw2',None)
        
        if not (username and password and re_password):
            res_data['error'] = "모든 값을 입력해야 합니다."
            return render(request, 'FaceDetection/signup.html', res_data)
        if password != re_password :
            res_data['error'] = '비밀번호가 다릅니다.'
            return render(request, 'FaceDetection/signup.html', res_data)
        else:
            user = User(uemail = username, upw=make_password(password))
            # res_data['error'] = "회원가입 성공"
            user.save()
    return render(request, 'FaceDetection/signup_complete.html', res_data) #signup을 요청받으면 signup.html 로 응답.

def login(request):
    response_data = {}

    if request.method == "GET" :
        return render(request, 'FaceDetection/login.html')

    elif request.method == "POST":
        login_username = request.POST.get('uemail', None)
        login_password = request.POST.get('upw', None)

        if not (login_username and login_password):
            response_data['error']="아이디와 비밀번호를 모두 입력해주세요."
        # if login_username != login_password:
        #     response_data['error']="회원가입이 필요한 서비스입니다." 
        
        else : 
            myuser = User.objects.get(uemail=login_username) 
            #db에서 꺼내는 명령. Post로 받아온 uemail로 , db의 uemail을 꺼내온다.
            if check_password(login_password, myuser.upw):
                request.session['user'] = myuser.id 
                request.session['uemail'] = myuser.uemail
                #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #세션 user라는 key에 방금 로그인한 id를 저장한것.
                return redirect('memolistview/')
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."

        return render(request, 'FaceDetection/login.html',response_data)

  
def logout(request):
    request.session.pop('uemail')
    return redirect('/')

def userpage(request):
    uemail=request.session.get('uemail')
    context={
        "uemail":request.session.get('uemail'),}
    return render(request, 'FaceDetection/userpage.html', context) 

from .forms import memoModelForm
def add_memo(request):
    form = memoModelForm(request.POST)
    if request.method =="POST":
        mname=request.POST.get('mname')
        mdetail=request.POST.get('mdetail')
        uemail=request.session.get('uemail')
        label=request.POST.get('label')
        budget=request.POST.get('budget')

        # 2. 입력값을 저장한다
        instance_memo=memo.objects.create( mname=mname, mdetail=mdetail, label=label, budget=budget, uemail=uemail, finished=False) #pdqty
        instance_memo.save()
    return redirect('memolist_view')


# 장볼 목록 페이지
def memolist_view(request):
    form = memoModelForm(request.POST)
    memo_list = memo.objects.filter(finished=False, uemail=request.session.get('uemail'))
    context = {
        "memo_list": memo_list,    
        "uemail":request.session.get('uemail'),
        "form": form
    }
    return render(request, "FaceDetection/memo_list.html", context)


def finishedlist_view(request):
    uemail=request.session.get('uemail')
    if request.method =="POST":
        cdate=request.POST.get('cdate')
    finished_memo_list = memo.objects.filter(finished=True)
    print(finished_memo_list)
    context = {
        'finished_memo_list': finished_memo_list,
        "uemail":request.session.get('uemail')
    }
    return render(request, "FaceDetection/finished_list.html", context)

def finish_list_item(request, id):
    finished_memo = get_object_or_404(memo, id=id)
    finished_memo.finished = True
    finished_memo.save()
    return redirect('memolist_view')

def delete_list_item(request, id):
    remove_memo = get_object_or_404(memo, id=id)
    remove_memo.delete()
    return redirect('memolist_view')

def recover_list_item(request, id):
    recover_memo = get_object_or_404(memo, id=id)
    recover_memo.finished = False
    recover_memo.save()
    return redirect('finishedlist_view')