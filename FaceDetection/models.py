from django.db import models

# Create your models here.
class ImageUploadModel(models.Model):
    #description = models.CharField(max_length=255, blank=True)
    document = models.ImageField(upload_to = 'images/%Y/%m/%d', verbose_name = '가격표')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    contents=models.CharField(max_length=500, blank=True)

from django.utils import timezone


class basket(models.Model):
    bsno = models.AutoField(primary_key=True)
    pdname = models.CharField(max_length=100)
    pdqty = models.IntegerField(default=1)
    pdprice=models.IntegerField()
    todo_id=models.IntegerField()
    done=models.IntegerField(default=1)


from django.db import models



class User(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    uemail = models.CharField(max_length=64,verbose_name = '사용자명')
    upw = models.CharField(max_length=128,verbose_name = '비밀번호')
    #registered_dttm = models.DateTimeField(auto_now_add=True,verbose_name='등록시간') 
    #저장되는 시점의 시간을 자동으로 삽입해준다.

    def __str__(self): # 이 함수 추가
        return self.uemail  # User object 대신 나타낼 문자 


    class Meta: #메타 클래스를 이용하여 테이블명 지정
        db_table = 'user'



LABLE_CHOICES = (
    ("primary", "기본"),
    ("success", "욕망의바구니"),
    ("danger", "중요"),
    ("warning", "기념일"),
    ("info", "회사"),
)

class memo(models.Model):
    mname = models.CharField(max_length=250, verbose_name="제목")
    cdate = models.DateField(default=timezone.now().strftime("%Y-%m-%d"), verbose_name="작성일")
    mdetail = models.TextField(max_length=1000, blank=True, verbose_name="내용")
    label = models.CharField(choices=LABLE_CHOICES, max_length=20, verbose_name="라벨")
    finished = models.BooleanField(default=False, verbose_name="계산완료")
    id = models.AutoField(primary_key=True)
    uemail = models.CharField(max_length=64,verbose_name = '사용자명')
    budget = models.IntegerField()
    class Meta:
        ordering = ["-cdate"]

