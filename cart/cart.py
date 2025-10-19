from decimal import Decimal
from django.conf import settings 
from main.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        
        # Простой способ получить цену
        price_value = product.sell_price() if product.discount > 0 else product.price
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 
                'price': str(price_value)  # Сохраняем как строку
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        self.session.modified = True
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            product_id = str(product.id)
            if product_id in self.cart:
                item = self.cart[product_id]
                # Всегда используем актуальную цену из базы
                current_price = product.sell_price() if product.discount > 0 else product.price
                
                yield {
                    'product': product,
                    'quantity': item['quantity'],
                    'price': Decimal(str(current_price)),
                    'total_price': Decimal(str(current_price)) * item['quantity']
                }
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()

    def get_total_price(self):
        total = Decimal('0')
        for item in self:
            total += item['total_price']
        return format(total, '.2f')