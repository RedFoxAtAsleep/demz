from django.contrib import admin
from someapp.models import Memo, Link

# Register your models here.


def get_simple_admin(model):
    name = "simple{}Admin".format(model.__name__)
    return type(name, (admin.ModelAdmin,), {'list_display': [f.name for f in model._meta.fields]})


admin.site.register(Memo, get_simple_admin(Memo))
admin.site.register(Link, get_simple_admin(Link))



