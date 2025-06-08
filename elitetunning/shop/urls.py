from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('book/', views.book, name='book'),
    path('cart/', views.cart, name='cart'),
    path('home/explore/', views.explore, name='explore'),
    path('account/', views.account, name='account'),
    path('shopcheckout/', views.shopcheckout, name='shopcheckout'),
    path('shopsuccess/', views.shopsuccess, name='shopsuccess'),
    #path('bookcheckout/', views.bookcheckout, name='bookcheckout'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('bookcheckout/<int:service_id>/', views.bookcheckout, name='bookcheckout'),
    path('booksuccess/', views.booksuccess, name='booksuccess'),
    path('orderhistory/', views.orderhistory, name='orderhistory'),
    path('bookhistory/', views.bookhistory, name='bookhistory'),

    
    
    



    #Fuctions urls
    path('update_item/', views.updateItem, name="update_item"),
    
    path('process_order/', views.processOrder, name='process_order'),

    path('process_booking/<int:service_id>/', views.process_booking, name='process_booking'),
    
]