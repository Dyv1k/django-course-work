from tabnanny import verbose

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):

    ADMIN = 'ADM'
    MANAGER = 'MAN'
    CLIENT = 'CLI'
    ROLES = [
        (ADMIN, 'Администратор'),
        (MANAGER, 'Менеджер'),
        (CLIENT, 'Клиент'),
    ]
    first_name = models.CharField('Фамилия', max_length=255)
    last_name = models.CharField('Имя', max_length=255)
    second_name = models.CharField('Отчество', max_length=255)
    phone = models.CharField('Номер телефона', max_length=18)
    role = models.CharField('Роль', max_length=20, choices=ROLES, default='CLI')
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CategoriesNews(models.Model):

    BUSINESS = 'BIS'
    INDUSTRY = 'IND'
    ANTI_CRISIS = 'ACR'
    CATEGORIES = [
        (BUSINESS, 'Бизнес'),
        (INDUSTRY, 'Промышленность'),
        (ANTI_CRISIS, 'Анти-кризис'),
    ]
    category = models.CharField('Категория новости', max_length=3, choices=CATEGORIES, default='BUSINESS')

    def __str__(self):
        if (self.category == self.BUSINESS):
            return 'Бизнес'
        elif (self.category == self.INDUSTRY):
            return 'Промышленность'
        elif (self.category == self.ANTI_CRISIS):
            return 'Анти-кризис'

    class Meta:
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'

class CategoriesServices(models.Model):

    ATTRACT_INVESTOR = 'ATR_INV'
    CREATE_FUNDING_STRATEGY = 'CREA_FUND_STAT'
    SEARCH_INVESTMENT_PROJECT = 'SEAR_INVEST_PROJ'
    CATEGORIES = [
        (ATTRACT_INVESTOR, 'Привлечь инвестора'),
        (CREATE_FUNDING_STRATEGY, 'Создание финансовой стратегии'),
        (SEARCH_INVESTMENT_PROJECT, 'Поиск инвестиционного проекта'),
    ]
    category = models.CharField('Категория услуги', max_length=20, choices=CATEGORIES, default='ATTRACT_INVESTOR')

    def __str__(self):
        if (self.category == self.ATTRACT_INVESTOR):
            return 'Привлечь инвестора'
        elif (self.category == self.CREATE_FUNDING_STRATEGY):
            return 'Создание финансовой стратегии'
        elif (self.category == self.SEARCH_INVESTMENT_PROJECT):
            return 'Поиск инвестиционного проекта'

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'

class News(models.Model):

    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    date_create = models.DateField('Дата создания', auto_now_add=True)
    photo = models.ImageField('Фото' ,upload_to='photos/%Y/%m/%d/', null=True)
    categories = models.ManyToManyField(CategoriesNews, verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("newsDetail", kwargs={"news_id": self.pk})
    

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering=['-date_create']

class Services(models.Model):

    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    price = models.PositiveIntegerField('Цена')
    photo = models.ImageField('Фото' ,upload_to='servicePhoto/%Y/%m/%d/', null=True)
    categories = models.ManyToManyField(CategoriesServices, verbose_name="Категория")
    date_create = models.DateField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.title}(id:{self.id})'

    def get_absolute_url(self):
        return reverse("servicesDetail", kwargs={"services_id": self.pk})

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering=['-date_create']

class NewsComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    news_item = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE, verbose_name="Выберите новость", blank=False)
    description = models.TextField('Комментарий', max_length=500)
    date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", blank=False)

    def __str__(self):
        return self.news_item.title

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering=['-date_create']

class Orders(models.Model):
    CREATED = 'CREAT'
    PAID = 'PAID'
    IN_PROGRESS = 'IN_PR'
    COMPLETE = 'COMPL'
    STATUS = [
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (IN_PROGRESS, 'На выполнении'),
        (COMPLETE, 'Выполнен'),
    ]
    status = models.CharField('Статус заказа', max_length=5, choices=STATUS, default='CREAT')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент", blank=False)
    services = models.ManyToManyField(Services, verbose_name="Услуги")
    date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    date_update = models.DateTimeField('Последнее изменение', auto_now=True)

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        return sum(service.price for service in self.services.all())

    get_total_cost.short_description = 'Сумма заказа'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering=['-date_create']