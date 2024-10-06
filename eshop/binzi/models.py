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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)  # Allow null temporarily
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


class Delivery(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    deliverer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'deliver'})
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending')
    location = models.CharField(max_length=255)  # Could include address and coordinates
    timestamp = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return f'Delivery for {self.sale.product.name} to {self.sale.user.username}'


class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_chat_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_chat_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class EShop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


# Rating for products
class ProductRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating out of 5
    comment = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.rating} stars by {self.user.username}'


# Rating for delivery users
class DeliverRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deliver_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='deliver_ratings', on_delete=models.CASCADE, limit_choices_to={'role': 'deliver'})
    rating = models.PositiveIntegerField()  # Rating out of 5
    comment = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Deliver {self.deliver_user.username} - {self.rating} stars by {self.user.username}'


# Rating for overall service quality
class ServiceQualityRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating out of 5
    comment = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Service quality - {self.rating} stars by {self.user.username}'


from django.utils import timezone

class PreCommandProduct(models.Model):
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('pending', 'Pending'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    official_release_date = models.DateField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='pre_command_products/', blank=True, null=True)
    video_publicity = models.FileField(upload_to='pre_command_videos/', blank=True, null=True)
    new_innovation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    eshop_location = models.CharField(max_length=255)  # The actual location can be captured here (e.g., GPS)

    def __str__(self):
        return self.name



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.code


class EmailCampaign(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Analytics(models.Model):
    date = models.DateField(auto_now_add=True)
    traffic = models.IntegerField()
    sales = models.DecimalField(max_digits=10, decimal_places=2)
    customer_behavior = models.JSONField()  # Store behavior as JSON

    def __str__(self):
        return f'Analytics for {self.date}'



class PreCommandTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(PreCommandProduct, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='non-paid')  # 'reserved' or 'paid'
    date = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
