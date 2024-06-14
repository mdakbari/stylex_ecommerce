from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Cart)
admin.site.register(stateModel)
admin.site.register(AddressModel)
admin.site.register(placeOrder)
admin.site.register(sub_placeorder)
admin.site.register(Contact)

admin.site.site_header = 'StyleX Admin'


