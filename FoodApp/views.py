from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem, Item
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'FoodApp/index.html')

def menu(request):
    cat1 = Item.objects.filter(category="I")
    cat2 = Item.objects.filter(category="IT")
    cat3 = Item.objects.filter(category="A")
    cat4 = Item.objects.filter(category="D")
    context = {
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
        'cat4': cat4,
    }
    return render(request, 'FoodApp/menu.html', context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("FoodApp:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("FoodApp:menu")
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("FoodApp:menu")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("FoodApp:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("FoodApp:menu")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("FoodApp:menu")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("FoodApp:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("FoodApp:menu")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("FoodApp:menu")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'FoodApp/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")
@login_required
def orders(request):
    order = Order.objects.filter(user=request.user, ordered=True)
    return render(request, 'FoodApp/orders.html', {'order': order})

@login_required
def confirmation(request):
    order = Order.objects.get(user=request.user, ordered=False)
    time = (Order.objects.filter(ordered=False).count() + 1)*15
    if order:
        context = {
            'object': True,
            'time': time
        }
    else:
        context = {
            'object': False,
            'time': time
        }
    return render(request, 'FoodApp/confirmation.html', context)