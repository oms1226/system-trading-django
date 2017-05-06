from django.db import models

# Create your models here.


class Stock(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=500)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

"""
야후
- 코스피 : 종목코드.KS
- 코스닥 : 종목코드.KQ

구글
- 코스피 : KRX:종목코드
- 코스닥 : KOSDAQ:종목코드
"""