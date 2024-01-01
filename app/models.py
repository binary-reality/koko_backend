from django.db import models

# Create your models here.


class user(models.Model):
    open_id = models.CharField(max_length=100, unique=True, blank=False)
    uid = models.BigAutoField(blank=False, primary_key=True, unique=True)
    create_time = models.DateField(auto_now_add=True)
    nickname = models.CharField(max_length=100, blank=False)
    headicon = models.ImageField(upload_to='./', default='./headicon.png')
    headicon_name = models.CharField(max_length=100, default='headicon.png')
    reserved_time = models.IntegerField(default=10)
    read_keep = models.IntegerField(default=1)
    wdlistnumber = models.IntegerField(default=0)
    followee = models.CharField(max_length=1000, blank=False)

    class Meta():
        verbose_name = "user_info"
        verbose_name_plural = verbose_name
        db_table = "user_info"


class rdrecord(models.Model):
    owner_openid = models.ForeignKey(
        to="user",
        to_field="open_id",
        on_delete=models.CASCADE,
        related_name='readingrecord')
    content = models.CharField(max_length=100, blank=False)
    rdnumber = models.IntegerField(default=0)
    cornumber = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    lastrd = models.CharField(max_length=100)
    lastres = models.IntegerField(default=0)

    class Meta():
        verbose_name = "reading_record"
        db_table = "reading_record"


class schrcd(models.Model):
    owner_openid = models.ForeignKey(
        to="user",
        to_field="open_id",
        on_delete=models.CASCADE,
        related_name='searchrecord')
    content = models.CharField(max_length=100, blank=False)
    schnumber = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)

    class Meta():
        verbose_name = "search_record"
        db_table = "search_record"


class wordlist_info(models.Model):
    owner_openid = models.ForeignKey(
        to="user",
        to_field="open_id",
        on_delete=models.CASCADE,
        related_name='wbinfo')
    name = models.CharField(max_length=100, default="默认单词本")
    index = models.IntegerField(blank=False)
    intro = models.CharField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='./wb/', default='./wb/default_wb.png')
    image_name = models.CharField(
        max_length=100,
        default='../../images/dictimage/dictimage3.png')
    date = models.DateField(auto_now_add=True)
    public_ctrl = models.IntegerField(default=0)       # 0 private 1 public

    class Meta():
        verbose_name = "wordlist_info"
        db_table = "wordlist_info"
        unique_together = ("owner_openid", "index")


class wordlist(models.Model):
    list_info = models.ForeignKey(
        "wordlist_info",
        on_delete=models.CASCADE,
        related_name='wordlist')
    content = models.CharField(max_length=100, blank=False)

    class Meta():
        verbose_name = "wordlist"
        db_table = "wordlist"


class flwordlist(models.Model):
    follower = models.ForeignKey(
        to='user',
        to_field='open_id',
        on_delete=models.CASCADE,
        related_name='flwbs')
    wb_info = models.ForeignKey(
        'wordlist_info',
        on_delete=models.CASCADE,
        related_name='follower_info')

    class Meta():
        verbose_name = "flwordlist"
        db_table = "flwordlist"
