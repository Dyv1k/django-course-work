from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from main import views
from leasing import settings

urlpatterns = [
    #admin panel page
    path('admin/', admin.site.urls, name='admin_panel'),
    #authenticate pages
    path('login', views.loginPage.as_view(), name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('registration', views.registrationPage.as_view(), name='registration'),
    #static pages
    path('', views.mainPage, name='main'),
    path('contacts', views.contactsPage, name='contacts'),
    #news pages
    path('news', views.newsPage.as_view(), name='news'),
    path('news/<int:news_id>', views.newsDetailPage.as_view(), name='newsDetail'),
    #service pages
    path('services', views.servicesPage.as_view(), name='services'),
    path('services/<int:services_id>/', views.servicesDetailPage.as_view(), name='servicesDetail'),
    path('services/<int:services_id>/<str:page>/add-cart', views.addCart, name='addCart'),
    #create pages
    path('create-news', views.createNewsPage, name='createNews'),
    path('create-services', views.createServicesPage, name='createServices'),
    #cart pages
    path('cart', views.cartPage, name='cart'),
    path('cart/<int:services_id>/remove', views.removeCart, name='removeCart'),
    path('cart/create-order', views.createOrder, name='createOrder'),
    #orders pages
    path('my-orders', views.myOrdersPage.as_view(), name='myOrdersPage'),
    path('orders', views.ordersPage.as_view(), name='ordersPage'),
    path('order/<int:orders_id>/pay', views.payOrder, name='payOrder'),
    path('order/<int:orders_id>/in-progress', views.inProgressOrder, name='inProgressOrder'),
    path('order/<int:orders_id>/complete', views.completeOrder, name='completeOrder'),
    path('order/<int:orders_id>/remove', views.removeOrder, name='removeOrder'),
    #users page (for Admin)
    path('users', views.usersPage.as_view(), name='usersPage'),
    path('users/<int:user_id>/remove', views.userRemove, name='userRemove'),
    path('users/<int:user_id>/set-role_<str:role>', views.userChangeRole, name='userChangeRole'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
