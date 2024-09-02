from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Add this import
from .views import chat_view, sales_analysis_view, manage_discounts
from .views import process_payment, download_receipt
from .views import publicity_feed, add_comment, toggle_like, toggle_favorite, book_publicity
from .views import contact_us, manage_messages, delete_contact_message, delete_contact, account_manage, order_history, loyalty_program
from .views import ManageDeliverView, DeliveryValidationView




urlpatterns = [
    path('', views.home, name='home'), # Root URL routed to the home view
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout, name='logout'),
    path('panel/admin/', views.admin_panel, name='admin_panel'),
    path('panel/deliver/', views.deliver_panel, name='deliver_panel'),
    path('panel/clients/', views.clients_panel, name='clients_panel'),
    path('clients/', views.clients_panel, name='clients_panel'),
    path('account/manage/', account_manage, name='account_manage'),
    path('order-history/', order_history, name='order_history'),
    path('loyalty_program/', loyalty_program, name='loyalty_program'),




    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


    path('manage_users/', views.manage_users, name='manage_users'),
    path('view_user/<int:user_id>/', views.view_user, name='view_user'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('manage_products/', views.manage_products, name='manage_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/view/<int:product_id>/', views.view_product, name='view_product'),  # New URL for viewing product details
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('about_us/', views.about_us, name='about_us'),
    path('chat/<int:recipient_id>/', chat_view, name='chat'),
    path('setting/', views.settings_view, name='setting'),
    path('analyse/', sales_analysis_view, name='analyse'),
    path('manage-discounts/', manage_discounts, name='manage_discounts'),
    path('manage_publicity', views.manage_publicity, name='manage_publicity'),
    path('add/', views.add_publicity, name='add_publicity'),
    path('edit/<int:pk>/', views.edit_publicity, name='edit_publicity'),
    path('delete/<int:pk>/', views.delete_publicity, name='delete_publicity'),
    path('manage-messages/', manage_messages, name='manage_messages'),
    path('delete-contact-message/<int:message_id>/', delete_contact_message, name='delete_contact_message'),
    path('delete-contact/<int:contact_id>/', delete_contact, name='delete_contact'),


    path('product_browsing/', views.product_browsing, name='product_browsing'),
    path('process-payment/', process_payment, name='process_payment'),
    path('download-receipt/<int:receipt_id>/', download_receipt, name='download_receipt'),

    path('publicity/', publicity_feed, name='publicity_feed'),
    path('publicity/<int:publicity_id>/comment/', add_comment, name='add_comment'),
    path('publicity/<int:publicity_id>/like/', toggle_like, name='toggle_like'),
    path('publicity/<int:publicity_id>/favorite/', toggle_favorite, name='toggle_favorite'),
    path('publicity/<int:publicity_id>/book/', book_publicity, name='book_publicity'),
    path('contact_us/', contact_us, name='contact_us'),


    path('manage-deliver/', ManageDeliverView.as_view(), name='manage_deliver'),
    path('validate-delivery/<int:pk>/', views.DeliveryValidationView.as_view(), name='validate_delivery'),




]