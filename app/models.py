from django.db import models

# Create your models here.

def create_my_wordlist(openid: str, index: int):
    list_field = {
        'list_id': models.IntegerField(blank=False),
        'owner_openid': models.ForeignKey("user", on_delete=models.CASCADE, related_name=str(index)),
        'content': models.CharField(max_length=100, blank=False),
        '__module__': __name__,
    }
    my_model = type(openid + "-" + str(index), (models.Model,), list_field)
    my_model._meta.db_table = openid + "-" + str(index)
    my_model._meta.app_label = "app"
    my_model._meta.model_name = "wordlist"
    my_model._meta.apps.register_model(app_label=my_model._meta.app_label, model=my_model)

    from django.db import connection
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor
    with BaseDatabaseSchemaEditor(connection) as editor:
        editor.create_model(model=my_model)
    return my_model



class user(models.Model):
    open_id = models.CharField(max_length=100, primary_key=True, unique=True, blank=False)
    create_time = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=0)
    class Meta():
        verbose_name = "user_info"
        verbose_name_plural = verbose_name
        db_table = "user_info"
