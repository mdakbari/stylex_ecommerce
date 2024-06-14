from django.db import models
from django.contrib.auth.models import User as User_1
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from admin_app.models import SubProduct
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
# from social_django.models import UserSocialAuth



class User(models.Model):
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def set_password(self, raw_password):
        self.user_password = make_password(raw_password)
        self.save()


    def __str__(self):
        time = (self.created_at + timedelta(hours=5, minutes=30)).strftime("%d/%b/%y %I:%M %p")
        if self.name:
            return f'{self.user_name} - {time}'
        # return f'{self.user_name}-{self.time}'

class Cart(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE)
    subproduct = models.ForeignKey(SubProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
            verbose_name_plural = 'Carts'
    
    def __str__(self):
        return f' {self.uname.user_name}- {self.subproduct.product.name} | {self.size} | {self.quantity}'



class stateModel(models.Model):
    state_name = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.state_name
        
class AddressModel(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    street_address = models.TextField(null=True)
    country = models.CharField(max_length=30, null=True, default='India')
    city = models.CharField(max_length=30, null=True)
    state = models.ForeignKey(stateModel, on_delete=models.CASCADE, null=True, blank=True)
    pincode = models.IntegerField(null=True)
    phone_number = models.BigIntegerField(null=True)
    email = models.CharField(max_length=30, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.user_id.user_name}'

class placeOrder(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address_id = models.ForeignKey(AddressModel, on_delete=models.CASCADE, null=True)
    payment_mode = models.CharField(max_length=50, null=True)
    order_date = models.DateField(blank=True, null=True)
    shipping_charge = models.IntegerField(null=True)
    total_quantity = models.IntegerField(null=True)
    total_amount = models.IntegerField(null=True)
    delivery_date = models.DateField(null=True)
    # transaction_id = models.CharField(max_length=30, blank=True, null=True)
    order_id = models.IntegerField(null=True)
    order_status = models.CharField(max_length=50, default='Pending')  

    def __str__(self):
        return f'{str(self.user_id.user_name)} | {str(self.order_id)}'

class sub_placeorder(models.Model):
    order_id = models.ForeignKey(placeOrder, on_delete=models.CASCADE, null=True)
    subproduct_id = models.ForeignKey(SubProduct, on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=50, null=True)
    size = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        time = (self.created_at + timedelta(hours=5, minutes=30)).strftime("%d/%b/%y %I:%M %p")
        return f'{self.order_id}  | {self.created_at}'
    

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    Comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        time = (self.created_at + timedelta(hours=5, minutes=30)).strftime("%d/%b/%y %I:%M %p")
        return f'{self.name} - {self.email} |  {time}'
    

class Visitor(models.Model):
    count = models.IntegerField(default=0)


    
    
@receiver(post_save, sender=User_1)
def create_or_update_user_model(sender, instance, created, **kwargs):
    if not User.objects.filter(user_name=instance.username):
        if instance.is_superuser:
            return

        if instance.first_name:
            obj = User()
            obj.name =  f'{instance.first_name} {instance.last_name}'
            obj.user_name = instance.username
            obj.user_email = instance.email
            obj.save()
