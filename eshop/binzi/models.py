from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings




class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('deliver', 'Deliver'),
        ('client', 'Client'),
    )
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='client')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    theme = models.CharField(max_length=100, default='light', choices=[('light', 'Light'), ('dark', 'Dark')])
    
class UserSetting(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    color_scheme = models.CharField(max_length=7, blank=True)  # Hex color code for the theme
    language = models.CharField(max_length=50, default='en')
    currency = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return f"Settings for {self.user.username}"
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Catalog(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('full_stock', 'Full Stock'),
        ('stock_alert', 'Stock Alert'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    max_quantity = models.IntegerField()
    min_quantity = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    catalog = models.ForeignKey('Catalog', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.calculate_status()
        super(Product, self).save(*args, **kwargs)

    def calculate_status(self):
        if self.quantity >= self.max_quantity:
            self.status = 'full_stock'
        elif self.quantity <= self.min_quantity:
            self.status = 'stock_alert'
        else:
            self.status = 'in_stock'

    def __str__(self):
        return self.name






    


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.product.price * self.quantity
        super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return f"Sale of {self.product.name} on {self.sale_date}"


    def calculate_discount(self):
        # Discount logic based on quantity
        if self.quantity >= 10:
            return 0.15  # 15% discount
        elif self.quantity >= 5:
            return 0.10  # 10% discount
        elif self.quantity >= 3:
            return 0.05  # 5% discount
        else:
            return 0.02  # 2% discount

    def final_price(self):
        discount = self.calculate_discount()
        return self.product.price * (1 - discount) * self.quantity




class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255)
    site_tagline = models.CharField(max_length=255, blank=True)
    site_logo = models.ImageField(upload_to='logos/', blank=True)
    site_favicon = models.ImageField(upload_to='favicons/', blank=True)
    color_scheme = models.CharField(max_length=7, blank=True)  # Hex color code
    site_font = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    social_media = models.URLField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    smtp_server = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=50, blank=True)
    currency = models.CharField(max_length=50, blank=True)
    custom_css = models.TextField(blank=True)
    custom_js = models.TextField(blank=True)  # Optional if needed


    
    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Receipt(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)  # E.g., "PayPal", "Credit Card"
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)  # E.g., "Completed", "Pending"

    def __str__(self):
        return f'Receipt {self.transaction_id} for {self.user.username}'
    






class Publicity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    photos = models.ManyToManyField('Photo', blank=True)
    videos = models.ManyToManyField('Video', blank=True)

    def __str__(self):
        return self.title

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or "Photo"

class Video(models.Model):
    video = models.FileField(upload_to='videos/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or "Video"

class Comment(models.Model):
    publicity = models.ForeignKey(Publicity, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.publicity}'

class Like(models.Model):
    publicity = models.ForeignKey(Publicity, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like by {self.user} on {self.publicity}'

class Favorite(models.Model):
    publicity = models.ForeignKey(Publicity, related_name='favorites', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Favorite by {self.user} on {self.publicity}'

class Booking(models.Model):
    publicity = models.ForeignKey(Publicity, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user} on {self.publicity}'
    


class Contact(models.Model):
    email = models.EmailField()
    description = models.TextField()
    service_rate = models.CharField(max_length=50)  # You can also use IntegerField with choices if it's a numeric rating
    date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.email