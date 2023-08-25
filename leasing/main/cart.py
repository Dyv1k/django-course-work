from django.conf import settings
from main.models import Services

class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        service_ids = self.cart.keys()
        services = Services.objects.filter(id__in=service_ids)
        for service in services:
            self.cart[str(service.id)]['service'] = service

        for item in self.cart.values():
            item['price'] = item['price']
            yield item

    def add(self, service):
        service_id = str(service.id)
        if service_id not in self.cart:
            self.cart[service_id] = {'price': str(service.price)}
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, service):
        service_id = str(service.id)
        if service_id in self.cart:
            del self.cart[service_id]
            self.save()

    def inCart(self, service):
        if str(service.id) not in self.cart:
            return False;
        else:
            return True;
    
    def get_total_price(self):
        # print(type(self.cart.values()))
        # print(self.cart)
        return sum(int(item['price']) for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True