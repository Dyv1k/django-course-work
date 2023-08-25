from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from main.cart import Cart
from main.forms import *

from .models import News, Services
from .static.appdata.contactsPage.data import contacts
from .static.appdata.mainConfig import mainConfig, topImages
from .static.appdata.mainPage.data import pageDescriptionObj

permissionError = '<h1 class="title">У вас нет прав на это действие!</h1>'

#mixins
class isClientUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return isClient(self.request.user)

    def handle_no_permission(self):
        return redirect('main')

class isPersonalUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return isPersonal(self.request.user)

    def handle_no_permission(self):
        return redirect('main')

class isAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return isAdmin(self.request.user)

    def handle_no_permission(self):
        return redirect('main')

# no pages functions
# ---------------------------------------------------------------------
def isPersonal(user):
    if isManager(user) or isAdmin(user):
        return True
    else: 
        return False

def isManager(user):
    if user.role == 'MAN':
        return True;
    else:
        return False;

def isAdmin(user):
    if user.role == 'ADM':
        return True;
    else:
        return False;

def isClient(user):
    if user.role == 'CLI':
        return True;
    else:
        return False;
# ---------------------------------------------------------------------
def setConfig(request, path=False):
    topImage = ''
    returnObj = {}

    for key, item in topImages.items():
        if not path :
            if (''.join(list(request.get_full_path().split('/')))) == key:
                topImage = item
        else: 
            if path == key:
                topImage = item
    if topImage: 
        returnObj = {**mainConfig, 'topImage': topImage}
    else: 
        returnObj = {**mainConfig, 'topImage': False}
    
    if request.user.is_authenticated:
        if isAdmin(request.user):
            returnObj = {**returnObj, 'role': 'Admin'}
        elif isManager(request.user):
            returnObj = {**returnObj, 'role': 'Manager'}
        elif isClient(request.user):
            returnObj = {**returnObj, 'role': 'Client', 'cartLength': len(Cart(request).cart)}
    else: returnObj = {**returnObj, 'role': 'Anonym'}

    return returnObj
# ---------------------------------------------------------------------
def addCart(request, services_id, page):
    if isClient(request.user):
        cart = Cart(request);
        service = get_object_or_404(Services, id=services_id)
        cart.add(service)
    if page == 'services':  
        return redirect('services')
    else:
        return redirect('servicesDetail', services_id=services_id)

def removeCart(request, services_id):
    if isClient(request.user):
        cart = Cart(request)
        service = get_object_or_404(Services, id=services_id)
        cart.remove(service)
    return redirect('cart')
# ---------------------------------------------------------------------
def createOrder(request):
    cart = Cart(request)
    order = Orders()
    order.user = request.user
    order.save()
    for item in [int(id) for id in list(cart.cart.keys())]:
        order.services.add(get_object_or_404(Services, id=item))
    cart.clear()
    return redirect('cart')

def removeOrder(request, orders_id):
    order = Orders.objects.get(id=orders_id)
    user = request.user
    if isPersonal(user):
        order.delete()
        return redirect('ordersPage')
    elif order.user == user:
        if order.status == 'CREAT':
            order.delete()
            return redirect('myOrdersPage')
        else:
            return HttpResponse('<h1 class="title">Для отмены оплаченного заказа обратитесь в поддержку!</h1>')
    else:
        return HttpResponse(permissionError)

def payOrder(request, orders_id):
    order = Orders.objects.get(id=orders_id)
    user = request.user
    if isPersonal(user):
        order.status = 'PAID'
        order.save()
        return redirect('ordersPage')
    elif order.user == user:
        if order.status == 'CREAT':
            order.status = 'PAID'
            order.save()
            return redirect('myOrdersPage')
        else:
            return HttpResponse('<h1 class="title">Вы уже оплатили данный заказ!</h1>')
    else:
        return HttpResponse(permissionError)

def inProgressOrder(request, orders_id):
    order = Orders.objects.get(id=orders_id)
    user = request.user
    if isPersonal(user):
        order.status = 'IN_PR'
        order.save()
        return redirect('ordersPage')
    else:
        return HttpResponse(permissionError)

def completeOrder(request, orders_id):
    order = Orders.objects.get(id=orders_id)
    user = request.user
    if isPersonal(user):
        order.status = 'COMPL'
        order.save()
        return redirect('ordersPage')
    else:
        return HttpResponse(permissionError)
# ---------------------------------------------------------------------
def userRemove (request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('usersPage')

def userChangeRole (request, user_id, role):
    user = get_object_or_404(User, id=user_id)
    if role == 'ADM':
        user.role = 'ADM'
    elif role == 'MAN':
        user.role = 'MAN'
    elif role == 'CLI':
        user.role = 'CLI'
    user.save()
    return redirect('usersPage')
# ---------------------------------------------------------------------
def logoutUser(request):
    logout(request)
    return redirect('login')
    
# pages functions
# ---------------------------------------------------------------------
def mainPage(request):
    news = News.objects.all()[:3]
    props = {
        'title': 'IFL Capital', 
        'news': news,
        'description': pageDescriptionObj,
        'mainConfig': setConfig(request),
    }
    return render(request, 'main/pages/mainPage/mainPage.html', props)
# ---------------------------------------------------------------------
class registrationPage(CreateView): 
    form_class = RegisterUserForm
    template_name = "main/pages/registrationPage/registrationPage.html"
    context_object_name: 'props'

    def form_valid(self, form):
        user_name = form.cleaned_data.get('username')
        user_password = form.cleaned_data.get('password2')
        user = form.save(commit=False)
        user.role = 'CLI'
        user.save()
        user = authenticate(username=user_name, password=user_password)
        login(self.request, user)
        return redirect('main')
    
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['mainConfig'] = setConfig(self.request, 'newsDetail')
        context['title'] = 'Регистрация'
        return context
# ---------------------------------------------------------------------
class loginPage(LoginView):
    form_class = LoginUserForm
    template_name = "main/pages/loginPage/loginPage.html"
    context_object_name: 'props'
    
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['mainConfig'] = setConfig(self.request, 'newsDetail')
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('main')
# ---------------------------------------------------------------------
class newsPage(ListView):
    model = News
    template_name = "main/pages/newsPage/newsPage.html"
    context_object_name = 'news'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['mainConfig'] = setConfig(self.request)
        context['title'] = 'Новости'
        context['categories'] = CategoriesNews.objects.all()
        context['form'] = FilterNewsForm()
        return context
    
    def get_queryset(self):
        if (self.request.GET.get('categories')):
            paramslist = []
            for item in CategoriesNews.objects.all():
                if item.category in self.request.GET.get('categories').split(','):
                    paramslist.append(item.pk)
            allNews = News.objects.filter(categories__in = paramslist).distinct()
        else:
            allNews = News.objects.get_queryset()
        return allNews

    def post(self, request, *args, **kwargs):
        category = request.POST.getlist('category')
        def setParams(paramsList):
            returnString = ''
            for (index, parametr) in enumerate(paramsList):
                print(parametr)
                if (index != len(paramsList)-1):
                    returnString += f'{parametr},'
                else:
                    returnString += f'{parametr}'
            return returnString
        params = setParams(category)
        if (len(params) != 0):
            return redirect(f'{reverse("news")}?categories={params}')
        else:
            return redirect('news')
# ---------------------------------------------------------------------
@user_passes_test(isPersonal, login_url='news')
def createNewsPage(request):
    if request.method == 'POST':
        form = CreateNewsForm(request.POST, request.FILES)
        if isPersonal(request.user):
            if form.is_valid():
                form.save()
                return redirect('news')
            else:
                form = CreateNewsForm()
        else:
            return HttpResponse(permissionError)
    else:
        form = CreateNewsForm()
    props = {
        'title': 'Добавить новость',
        'mainConfig': setConfig(request),
        'form': form
    }
    return render(request, 'main/pages/createNewsPage/createNewsPage.html', props)
# ---------------------------------------------------------------------
class newsDetailPage(DetailView):
    model = News
    template_name = "main/pages/detailPage/detailPage.html"
    pk_url_kwarg = 'news_id'
    context_object_name: 'props'
    http_method_names = ['post', 'get']

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['mainConfig'] = setConfig(self.request, 'newsDetail')
        print(self.get_object())
        if self.request.user.is_authenticated:
            context['addCommentform'] = CreateNewsComment()
            
        return context

    def post(self, request, *args, **kwargs):
        form = CreateNewsComment(request.POST)
        if form.is_valid():
                comment = NewsComments()
                comment.news_item_id = self.get_object().id
                comment.creator_id = self.request.user.id
                comment.description = form.cleaned_data['description']
                comment.save()
                return redirect('newsDetail', news_id=self.get_object().id)
        return redirect('newsDetail', news_id=self.get_object().id)
            
# ---------------------------------------------------------------------
class servicesPage(ListView):
    model = Services
    template_name = "main/pages/servicesPage/servicesPage.html"
    context_object_name = 'services'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['mainConfig'] = setConfig(self.request)
        context['title'] = 'Каталог услуг'
        context['cart'] =  [int(id) for id in list(Cart(self.request).cart.keys())] 
        context['categories'] = CategoriesNews.objects.all()
        context['form'] = FilterServicesForm()
        return context
    
    def get_queryset(self):
        if (self.request.GET.get('categories')):
            paramslist = []
            for item in CategoriesServices.objects.all():
                if item.category in self.request.GET.get('categories').split(','):
                    paramslist.append(item.pk)
            allNews = Services.objects.filter(categories__in = paramslist).distinct()
        else:
            allNews = Services.objects.get_queryset()
        return allNews

    def post(self, request, *args, **kwargs):
        category = request.POST.getlist('category')
        def setParams(paramsList):
            returnString = ''
            for (index, parametr) in enumerate(paramsList):
                print(parametr)
                # returnString+=f'{parametr},'
                if (index != len(paramsList)-1):
                    returnString += f'{parametr},'
                else:
                    returnString += f'{parametr}'
            return returnString
        params = setParams(category)
        if (len(params) != 0):
            return redirect(f'{reverse("services")}?categories={params}')
        else:
            return redirect('services')
# ---------------------------------------------------------------------
@user_passes_test(isPersonal, login_url='services')
def createServicesPage(request):
    if request.method == 'POST':
        form = CreateServicesForm(request.POST, request.FILES)
        if isPersonal(request.user):
            if form.is_valid():
                form.save()
                return redirect('services')
            else:
                form = CreateServicesForm()
        else:
            return HttpResponse(permissionError)
    else:
        form = CreateServicesForm()
    props = {
        'title': 'Добавить услугу',
        'mainConfig': setConfig(request),
        'form': form
    }
    return render(request, 'main/pages/createServicesPage/createServicesPage.html', props)
# ---------------------------------------------------------------------
class servicesDetailPage(DetailView):
    model = Services
    template_name = "main/pages/detailPage/detailPage.html"
    pk_url_kwarg = 'services_id'
    context_object_name: 'props'
    http_method_names = ['post', 'get']
    
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['mainConfig'] = setConfig(self.request, 'servicesDetail')
        context['inCart'] = Cart.inCart(Cart(self.request), get_object_or_404(Services, id=self.kwargs.get('services_id')))
        return context
# ---------------------------------------------------------------------
def contactsPage(request):
    props = {
        'title': 'Контакты', 
        'contacts': contacts,
        'mainConfig': setConfig(request),
    }
    return render(request, 'main/pages/contactsPage/contactsPage.html', props)
# ---------------------------------------------------------------------
@user_passes_test(isClient, login_url='main')
def cartPage(request):
    cart = Cart(request)
    props = {
        'title': 'Корзина', 
        'cart': cart,
        'mainConfig': setConfig(request),
    }
    return render(request, 'main/pages/cart/cart.html', props)
# ---------------------------------------------------------------------
class ordersPage(isPersonalUserMixin, ListView):
    model = Orders
    template_name = "main/pages/ordersPage/ordersPage.html"
    context_object_name = 'orders'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['mainConfig'] = setConfig(self.request)
        context['title'] = 'Заказы'
        return context
# ---------------------------------------------------------------------
class myOrdersPage(isClientUserMixin, ListView):
    model = Orders
    template_name = "main/pages/ordersPage/ordersPage.html"
    context_object_name = 'orders'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['mainConfig'] = setConfig(self.request)
        context['title'] = 'Мои заказы'
        return context

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)
# ---------------------------------------------------------------------
class usersPage(isAdminMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = "main/pages/usersPage/usersPage.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['mainConfig'] = setConfig(self.request)
        context['title'] = 'Пользователи'
        context['roles'] = ['ADM', 'MAN', 'CLI']
        return context