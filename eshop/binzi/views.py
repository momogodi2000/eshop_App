from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, ForgotPasswordForm
from .models import CustomUser, AbstractUser # Updated import
from .tokens import account_activation_token
from .forms import RegistrationForm, ForgotPasswordForm
from .models import Product
from .forms import ProductForm
from .models import SiteSettings
from django.db.models import Sum
from django.utils import timezone
from .models import Sale, Message
from .models import Category, Catalog
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Receipt
from django.conf import settings
import campay
from campay.sdk import Client as CamPayClient
from django.core.files.base import ContentFile
from .models import Publicity, Video, Photo
from .forms import PublicityForm, VideoForm, PhotoForm
from .models import  Comment, Like, Favorite, Booking
from .forms import CustomUserChangeForm, UserSettingForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserSetting
from .forms import ContactForm  # Correct import from forms.py










# Function to generate a random 6-digit password reset code
def generate_password_reset_code():
    import random
    code = ''.join(str(random.randint(0, 9)) for _ in range(6))
    return code


class CustomPasswordResetView(PasswordResetView):
    template_name = 'auth/forgot_password.html'  # Customize the forgot password template
    success_url = reverse_lazy('password_reset_done')  # Redirect URL after sending email
    email_template_name = 'auth/password_reset_email.html'  # Customize the reset email template

    def form_valid(self, form):
        user = form.save()
        password_reset_code = generate_password_reset_code()
        user.set_password(password_reset_code)  # Set temporary password
        user.save()

        # Generate password reset token
        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(self.request)
        domain = current_site.domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        relative_link = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        absolute_link = f'http://{domain}{relative_link}'

        # Render email content with password reset link
        email_body = render_to_string(self.email_template_name, {
            'user': user,
            'reset_link': absolute_link,
            'password_reset_code': password_reset_code,  # Include the code for reference
        })

        send_mail(
            subject='Password Reset Request (My E-commerce Platform)',
            message=email_body,
            from_email='your_email@example.com',  # Replace with your email
            recipient_list=[user.email],
            fail_silently=False,
        )

        return redirect(self.get_success_url())


def home(request):
    return render(request, 'home/home.html')


def contact(request):
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.role == 'admin':
                return redirect('admin_panel')  # Adjust this to match your URL pattern name
            elif user.role == 'deliver':
                return redirect('deliver_panel')  # Adjust this to match your URL pattern name
            else:
                return redirect('clients_panel')  # Adjust this to match your URL pattern name
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetView.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_done')  # Redirect to success page
    else:
        form = CustomPasswordResetView.form_class()

    return render(request, 'auth/forgot_password.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')

# dashboard

@login_required
def admin_panel(request):
    total_users = CustomUser.objects.count()
    total_products = Product.objects.count()
    total_sales = Sale.objects.count()  # Assuming Sale represents completed orders
    chat_with_delivery = Message.objects.filter(sender__role='deliver').count()  # Assuming 'deliver' role in sender

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_sales': total_sales,
        'chat_with_delivery': chat_with_delivery,
    }
    return render(request, 'panel/admin/admin_panel.html')

@login_required
def deliver_panel(request):
    return render(request, 'panel/deliver/deliver_panel.html')

@login_required
def clients_panel(request):
    return render(request, 'panel/clients/clients_panel.html')

#crud_user

@login_required
def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'panel/admin/manage_users.html', {'users': users})

@login_required
def view_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'panel/admin/crud_user/view_user.html', {'user': user})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user to the database
            user = form.save(commit=False)  # Create user instance but don't save it yet
            user.save()  # Now save the user to the database

            # Optionally add more user setup here, such as assigning roles, sending emails, etc.

            messages.success(request, f'User {user.username} was successfully added!')
            return redirect('manage_users')  # Replace with your actual URL name
        else:
            messages.error(request, 'There was an error with the form. Please correct the errors and try again.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'panel/admin/crud_user/add_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'panel/admin/crud_user/edit_user.html', {'form': form})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    return render(request, 'panel/admin/crud_user/delete_user.html', {'user': user})

#crud_product

@login_required
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'panel/admin/manage_products.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.calculate_status()  # Calculate status before saving
            
            # Set the category and catalog from the form choices
            product.category = form.cleaned_data['category']
            product.catalog = form.cleaned_data['catalog']
            
            product.save()
            messages.success(request, f'Product "{product.name}" has been added successfully!')
            return redirect('manage_products')
        else:
            messages.error(request, 'There was an error with the form. Please correct the errors and try again.')
    else:
        form = ProductForm()

    return render(request, 'panel/admin/crud_product/add_product.html', {
        'form': form
    })


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.calculate_status()  # Recalculate status before saving
            product.save()
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'panel/admin/crud_product/edit_product.html', {'form': form, 'product': product})

@login_required
def view_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'crud_product/view_product.html', {'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('manage_products')
    return render(request, 'panel/admin/crud_product/delete_product.html', {'product': product})

@login_required
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'panel/admin/crud_product/view_product.html', {'product': product})

def about_us(request):
    return render(request, 'panel/admin/about_us.html')


@login_required
def chat_view(request, recipient_id):
    recipient = get_object_or_404(CustomUser, id=recipient_id)
    return render(request, 'panel/admin/chat/chat.html', {'recipient': recipient})

@login_required
def settings_view(request):
    try:
        settings = SiteSettings.objects.get(id=1)  # Attempt to get object with ID 1
    except SiteSettings.DoesNotExist:
        # Create a new settings object if it doesn't exist
        settings = SiteSettings.objects.create(
            site_name="Your Website Name",  # Set default values
            # ... other default settings
        )

    if request.method == 'POST':
        # Process the form data
        site_name = request.POST.get('siteName')
        site_tagline = request.POST.get('siteTagline')
        contact_email = request.POST.get('contactEmail')
        contact_phone = request.POST.get('contactPhone')
        social_media = request.POST.get('socialMedia')
        meta_title = request.POST.get('metaTitle')
        meta_description = request.POST.get('metaDescription')
        meta_keywords = request.POST.get('metaKeywords')
        smtp_server = request.POST.get('smtpServer')
        language = request.POST.get('language')
        currency = request.POST.get('currency')
        custom_css = request.POST.get('customCss')

        # Handle file uploads
        if 'siteLogo' in request.FILES:
            settings.site_logo = request.FILES['siteLogo']
        if 'siteFavicon' in request.FILES:
            settings.site_favicon = request.FILES['siteFavicon']

        # Update settings fields
        settings.site_name = site_name
        settings.site_tagline = site_tagline
        settings.contact_email = contact_email
        settings.contact_phone = contact_phone
        settings.social_media = social_media
        settings.meta_title = meta_title
        settings.meta_description = meta_description
        settings.meta_keywords = meta_keywords
        settings.smtp_server = smtp_server
        settings.language = language
        settings.currency = currency
        settings.custom_css = custom_css

        # Save changes
        settings.save()

        # Redirect to the settings page (or show a success message)
        return redirect('settings_view')  # Replace with the correct URL name

    # Render the settings page
    return render(request, 'panel/admin/setting/setting.html', {'settings': settings})

@login_required
def sales_analysis_view(request):
    # Get current year and month
    now = timezone.now()
    current_year = now.year
    current_month = now.month

    # Monthly sales data
    monthly_sales = Sale.objects.filter(
        sale_date__year=current_year
    ).values('sale_date__month').annotate(
        total_sales=Sum('total_amount')
    ).order_by('sale_date__month')

    # Yearly sales data
    yearly_sales = Sale.objects.values('sale_date__year').annotate(
        total_sales=Sum('total_amount')
    ).order_by('sale_date__year')

    context = {
        'monthly_sales': monthly_sales,
        'yearly_sales': yearly_sales,
    }
    return render(request, 'panel/admin/setting/analyse.html', context)


@login_required
def manage_discounts(request):
    sales = Sale.objects.all()
    for sale in sales:
        sale.discount_percentage = sale.calculate_discount * 100
        sale.final_price = sale.product.price - (sale.product.price * sale.calculate_discount)
    
    return render(request, 'panel/admin/setting/manage_discounts.html', {
        'sales': sales,
    })





# panel/admin/crud_pub/views.py

@login_required
def manage_publicity(request):
    publicities = Publicity.objects.all()
    return render(request, 'panel/admin/crud_pub/manage_publicity.html', {'publicities': publicities})

@login_required
def add_publicity(request):
    if request.method == 'POST':
        form = PublicityForm(request.POST, request.FILES)
        if form.is_valid():
            publicity = form.save()
            photos = request.FILES.getlist('photos')
            for photo in photos:
                new_photo = Photo.objects.create(image=photo)
                publicity.photos.add(new_photo)
            videos = request.FILES.getlist('videos')
            for video in videos:
                new_video = Video.objects.create(video=video)
                publicity.videos.add(new_video)
            return redirect('manage_publicity')
    else:
        form = PublicityForm()
    return render(request, 'panel/admin/crud_pub/add_publicity.html', {'form': form})

@login_required
def edit_publicity(request, pk):
    publicity = get_object_or_404(Publicity, pk=pk)
    if request.method == 'POST':
        form = PublicityForm(request.POST, request.FILES, instance=publicity)
        if form.is_valid():
            publicity = form.save()
            publicity.photos.clear()
            publicity.videos.clear()
            photos = request.FILES.getlist('photos')
            for photo in photos:
                new_photo = Photo.objects.create(image=photo)
                publicity.photos.add(new_photo)
            videos = request.FILES.getlist('videos')
            for video in videos:
                new_video = Video.objects.create(video=video)
                publicity.videos.add(new_video)
            return redirect('manage_publicity')
    else:
        form = PublicityForm(instance=publicity)
    return render(request, 'panel/admin/crud_pub/edit_publicity.html', {'form': form, 'publicity': publicity})

@login_required
def delete_publicity(request, pk):
    publicity = get_object_or_404(Publicity, pk=pk)
    if request.method == 'POST':
        publicity.delete()
        return redirect('manage_publicity')
    return render(request, 'panel/admin/crud_pub/delete_publicity.html', {'publicity': publicity})







#clients logic/view

@login_required
def product_browsing(request):
    # Get all categories and catalogs
    categories = Category.objects.all()
    catalogs = Catalog.objects.all()

    # Get the selected category and catalog from the request
    selected_category = request.GET.get('category')
    selected_catalog = request.GET.get('catalog')

    # Filter products based on the selected category and catalog
    products = Product.objects.all()
    if selected_category:
        products = products.filter(category__id=selected_category)
    if selected_catalog:
        products = products.filter(catalog__id=selected_catalog)

    return render(request, 'panel/clients/product/product_browsing.html', {
        'products': products,
        'categories': categories,
        'catalogs': catalogs,
        'selected_category': selected_category,
        'selected_catalog': selected_catalog,
    })






##payment API

campay = CamPayClient({
    "app_username": "JByBUneb4BceuEyoMu1nKlmyTgVomd-QfokOrs4t4B9tPJS7hhqUtpuxOx5EQ7zpT0xmYw3P6DU6LU0mH2DvaQ",
    "app_password": "m-Xuj9EQIT_zeQ5hSn8hLjYlyJT7KnSTHABYVp7tKeHKgsVnF0x6PEcdtZCVaDM0BN5mX-eylX0fhrGGMZBrWg",
    "environment": "PROD"  # use "DEV" for demo mode or "PROD" for live mode
})


def process_payment(request):
    if request.method == 'POST':
        try:
            # Parse JSON request data
            data = json.loads(request.body)
            payment_method = data.get('paymentMethod')
            cart_items = data.get('cartItems')
            cart_total = data.get('cartTotal')
            phone_number = data.get('phoneNumber')  # Phone number for the payment

            # Process payment with CamPay
            collect = campay.collect({
                "amount": str(cart_total),  # Ensure cart_total is a string
                "currency": "XAF",
                "from": "237" + phone_number,  # Include country code
                "description": "Purchase Payment",
                "external_reference": "",  # Can be a unique transaction ID from your system
            })

            # Check if payment was successful
            if collect.get('status') == 'SUCCESSFUL':
                # Generate receipt
                receipt_id = generate_receipt(cart_items, cart_total)
                return JsonResponse({'success': True, 'receiptId': receipt_id})
            else:
                # Handle payment failure
                return JsonResponse({'success': False, 'message': collect.get('reason', 'Payment failed')}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

@login_required
def generate_receipt(cart_items, cart_total):
    # Create a receipt object and save it to the database
    receipt = Receipt.objects.create(total=cart_total)

    # Generate PDF receipt
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    html = render_to_string('panel/clients/product/receipt.html', context)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=result)

    if not pdf.err:
        receipt_file = ContentFile(result.getvalue())
        receipt.pdf.save(f'receipt_{receipt.id}.pdf', receipt_file)
        return receipt.id

    return None


@login_required
def download_receipt(request, transaction_id):
    # Retrieve the receipt object based on the transaction_id
    receipt = get_object_or_404(Receipt, transaction_id=transaction_id)

    # Render the receipt template with receipt data
    html = render_to_string('panel/clients/product/receipt.html', {'receipt': receipt})

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{transaction_id}.pdf"'

    # Convert HTML to PDF and write to response
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response





@login_required
def publicity_feed(request):
    publicities = Publicity.objects.all().order_by('-date_posted')
    return render(request, 'panel/clients/social/publicity_feed.html', {'publicities': publicities})

@login_required
def add_comment(request, publicity_id):
    publicity = get_object_or_404(Publicity, id=publicity_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(publicity=publicity, user=request.user, content=content)
    return redirect('publicity_feed')

@login_required
def toggle_like(request, publicity_id):
    publicity = get_object_or_404(Publicity, id=publicity_id)
    like, created = Like.objects.get_or_create(publicity=publicity, user=request.user)
    if not created:
        like.delete()
    return redirect('publicity_feed')

@login_required
def toggle_favorite(request, publicity_id):
    publicity = get_object_or_404(Publicity, id=publicity_id)
    favorite, created = Favorite.objects.get_or_create(publicity=publicity, user=request.user)
    if not created:
        favorite.delete()
    return redirect('publicity_feed')

@login_required
def book_publicity(request, publicity_id):
    publicity = get_object_or_404(Publicity, id=publicity_id)
    Booking.objects.create(publicity=publicity, user=request.user)
    return redirect('publicity_feed')






@login_required
def account_management(request):
    user = request.user
    try:
        user_setting = user.usersetting
    except UserSetting.DoesNotExist:
        # Create the UserSetting object if it doesn't exist
        user_setting = UserSetting.objects.create(user=user)
    
    context = {
        'user_setting': user_setting,
        'user': user,
    }
    return render(request, 'panel/clients/setting/account_management.html', context)



@receiver(post_save, sender=CustomUser)
def create_user_setting(sender, instance, created, **kwargs):
    if created:
        UserSetting.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_setting(sender, instance, **kwargs):
    instance.usersetting.save()





def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('contact_us')  # Redirect to success page
    else:
        form = ContactForm()
        return render(request, 'panel/clients/setting/contact_us.html', {'form': form})

