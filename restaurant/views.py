from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import OrderModel

# Create your views here.
class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):

        # get the current date
        current = self.request.user.get_username()
        today = datetime.today()
        orders = OrderModel.objects.filter(created_on__year= today.year,
        created_on__month= today.month , created_on__day = today.day)

        # loop through the orders and add the price value and place only  shipped orders on our dashboard
        total_revenue = 0
        order_unshipped = []
        for order in orders:
            total_revenue += order.price

            if not order.is_shipped:
                order_unshipped.append(order)
        # pass parameters into conttext
        context= {
            'current': current,
            'orders': order_unshipped,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'restaurant/dashboard.html', context)
    # to test if any user logging in is our list of authoriseds
    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order= OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'order': order
        }
        return render(request, 'restaurant/order-details.html', context)


    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

   
    

