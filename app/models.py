from django.db import models

# Create your models here.

# def create_my_wordlist(index: int):
#     list_field = {
#         'owner_openid': models.ForeignKey(to="user", to_field="open_id", on_delete=models.CASCADE, related_name='list' + str(index)),
#         'content': models.CharField(max_length=100, blank=False),
#         '__module__': __name__,
#     }
#     model_name = "list" + str(index)
#     my_model = type(model_name, (models.Model,), list_field)
#     my_model._meta.db_table = model_name
#     my_model._meta.app_label = "app"
#     my_model._meta.model_name = model_name
#     my_model._meta.apps.register_model(app_label=my_model._meta.app_label, model=my_model)

#     from django.db import connection
#     from django.db.backends.base.schema import BaseDatabaseSchemaEditor
#     with BaseDatabaseSchemaEditor(connection) as editor:
#         editor.create_model(model=my_model)
#     return my_model

# def create_my_readingrecord(openid: str):
#     list_field = {
#         'owner_openid': models.ForeignKey(to="user", to_field="open_id", on_delete=models.CASCADE, related_name='readingrecord'),
#         'content': models.CharField(max_length=100, blank=False),
#         'rdnumber': models.IntegerField(default=0),
#         'cornumber': models.IntegerField(default=0),
#         'date': models.DateField(auto_now=True),
#         'lastrd': models.CharField(max_length=100),
#         'lastres': models.IntegerField(default=0),
#         '__module__': __name__,
#     }
#     model_name = openid + "-readingrecord"
#     my_model = type(model_name, (models.Model,), list_field)
#     my_model._meta.db_table = model_name
#     my_model._meta.app_label = "app"
#     my_model._meta.model_name = model_name
#     my_model._meta.apps.register_model(app_label=my_model._meta.app_label, model=my_model)

#     from django.db import connection
#     from django.db.backends.base.schema import BaseDatabaseSchemaEditor
#     with BaseDatabaseSchemaEditor(connection) as editor:
#         editor.create_model(model=my_model)
#     return my_model

# def create_my_searchrecord(openid: str):
#     list_field = {
#         'owner_openid': models.ForeignKey(to="user", to_field="open_id", on_delete=models.CASCADE, related_name='searchrecord'),
#         'content': models.CharField(max_length=100, blank=False),
#         'schnumber': models.IntegerField(default=0),
#         'date': models.DateField(auto_now=True),
#         '__module__': __name__,
#     }
#     model_name = openid + "-searchrecord"
#     my_model = type(model_name, (models.Model,), list_field)
#     my_model._meta.db_table = model_name
#     my_model._meta.app_label = "app"
#     my_model._meta.model_name = model_name
#     my_model._meta.apps.register_model(app_label=my_model._meta.app_label, model=my_model)

#     from django.db import connection
#     from django.db.backends.base.schema import BaseDatabaseSchemaEditor
#     with BaseDatabaseSchemaEditor(connection) as editor:
#         editor.create_model(model=my_model)
#     return my_model

# def create_my_wordlistinfo(openid: str):
#     list_field = {
#         'owner_openid': models.ForeignKey(to="user", to_field="open_id", on_delete=models.CASCADE, related_name='wbinfo'),
#         'name': models.CharField(max_length=100, blank=False),
#         'intro': models.CharField(max_length=1000, blank=True),
#         'image': models.ImageField(upload_to='./wb/' + openid, default='./headicon.png'),
#         'date': models.DateField(auto_now_add=True),
#         '__module__': __name__,
#     }
#     model_name = openid + "-wbinfo"
#     my_model = type(model_name, (models.Model,), list_field)
#     my_model._meta.db_table = model_name
#     my_model._meta.app_label = "app"
#     my_model._meta.model_name = model_name
#     my_model._meta.apps.register_model(app_label=my_model._meta.app_label, model=my_model)

#     from django.db import connection
#     from django.db.backends.base.schema import BaseDatabaseSchemaEditor
#     with BaseDatabaseSchemaEditor(connection) as editor:
#         editor.create_model(model=my_model)
#     return my_model

class user(models.Model):
    open_id = models.CharField(max_length=100, unique=True, blank=False)
    uid = models.BigAutoField(blank=False, unique=True)
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
        unique_together = ("openid", "uid")

class rdrecord(models.Model):
    owner_openid = models.ForeignKey(to="user", to_field="open_id", on_delete=models.CASCADE, related_name='readingrecord')
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
    owner_openid = models.ForeignKey(to="user", to_field="open_id", on_delete=models.CASCADE, related_name='searchrecord')
    content = models.CharField(max_length=100, blank=False)
    schnumber = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    class Meta():
        verbose_name = "search_record"
        db_table = "search_record"

class wordlist_info(models.Model):
    owner_openid = models.ForeignKey(to="user", to_field="open_id", on_delete=models.CASCADE, related_name='wbinfo')
    name = models.CharField(max_length=100, default="默认单词本")
    index = models.IntegerField(blank=False)
    intro = models.CharField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='./wb/', default='./wb/default_wb.png')
    image_name = models.CharField(max_length=100, default='../../images/dictimage/dictimage3.png')
    date = models.DateField(auto_now_add=True)
    class Meta():
        verbose_name = "wordlist_info"
        db_table = "wordlist_info"
        unique_together = ("owner_openid", "index")

class wordlist(models.Model):
    list_info = models.ForeignKey("wordlist_info", on_delete=models.CASCADE, related_name='wordlist')
    content = models.CharField(max_length=100, blank=False)
    class Meta():
        verbose_name = "wordlist"
        db_table = "wordlist"
