from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import CustomUser
from .models import Product
from django import forms
from .models import Product, Category, Catalog
from .models import Publicity, Video, Photo
from django.contrib.auth.forms import UserChangeForm
from .models import Contact


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Updated model
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser  # Updated model
        fields = UserCreationForm.Meta.fields= ['username', 'email', 'role','password1', 'password2']
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()





# Define the choices for categories and catalogs
CATEGORIES_CHOICES = [
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Home & Kitchen', 'Home & Kitchen'),
    ('Books', 'Books'),
    ('Beauty & Personal Care', 'Beauty & Personal Care'),
    ('Toys & Games', 'Toys & Games'),
    ('Sports & Outdoors', 'Sports & Outdoors'),
    ('Food & Beverages', 'Food & Beverages'),
    ('Automotive', 'Automotive'),
    ('Furniture', 'Furniture'),
]

CATALOGS_CHOICES = [
    ('Digital clothing catalog', 'Digital clothing catalog'),
    ('Grocery store online catalog', 'Grocery store online catalog'),
    ('Book retailer\'s catalog', 'Book retailer\'s catalog'),
    ('Furniture catalog', 'Furniture catalog'),
]

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    catalog = forms.ModelChoiceField(
        queryset=Catalog.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'max_quantity', 'min_quantity', 'image', 'price', 'category', 'catalog']



class GeneralSettingsForm(forms.Form):
    site_name = forms.CharField(max_length=100, label='Site Name')
    site_tagline = forms.CharField(max_length=255, label='Site Tagline', required=False)
    site_logo = forms.ImageField(label='Site Logo', required=False)
    site_favicon = forms.ImageField(label='Site Favicon', required=False)
    color_scheme = forms.CharField(max_length=7, label='Color Scheme', required=False)
    font = forms.CharField(max_length=50, label='Font', required=False)
    contact_email = forms.EmailField(label='Contact Email', required=False)
    contact_phone = forms.CharField(max_length=20, label='Contact Phone', required=False)
    social_media_links = forms.URLField(label='Social Media Links', required=False)





from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'multiple_uploads.html'  # Create a custom template

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['multiple'] = 'multiple'  # Add multiple attribute
        return context



class PublicityForm(forms.ModelForm):
    class Meta:
        model = Publicity
        fields = ['title', 'description']
        # Remove 'photos' and 'videos' from the fields as they will be handled separately

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video', 'description']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }




class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'theme']




class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'description', 'service_rate', 'date', 'location']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'service_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),

        }