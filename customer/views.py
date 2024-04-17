import json
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View 
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel
from django.http import JsonResponse

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):

        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains= 'Appetizer')
        entres = MenuItem.objects.filter(category__name__contains= 'Entre')
        desserts = MenuItem.objects.filter(category__name__contains= 'Dessert')
        drinks = MenuItem.objects.filter(category__name__contains= 'Drink')

        
        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')  # To grab values of fields we set on our 
        email = request.POST.get('email') # html (form method), we need to post them in our views
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        
        
        

        order_items = {
            'items': []
        }
        

        items = self.request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains= int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }   

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        
        
        order = OrderModel.objects.create(
            price=price, 
            name=name, # adding more values to our order. creating...
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # after everything is done, we then send emails.
       
        body =('Thank you for your order! Your food is being made!\n'
        f'Total:{price}\n'
        'Thank You Again For Your Order!') # body message to be sent to RECIPIENT_
        
        send_mail(
            'Thank You For Your Order!',
            body,
            'example@company.com',
            [email],
            fail_silently= True,
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect( 'order-confirmation' , pk= order.pk)
    



class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):

        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price
        }

        return render(request, 'customer/order_confirmation.html', context)


    def post(self, pk, *args, **kwargs):
        data = json.loads(self.request.body)

        if data['isPaid']:
            order= OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()
            
        return redirect('payment-confirmation')




class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }
        return render(request, 'customer/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items= MenuItem.objects.filter(
            Q(name__icontains=query)|
            Q(price__icontains=query)|
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }
        return render(request, 'customer/menu.html', context)




    
