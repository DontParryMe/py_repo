import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customers.models import Customer
from orders.forms import OrderForm
from orders.models import Order


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = OrderForm(data)
        if form.is_valid():
            customer_email = form.cleaned_data['customer']
            model = form.cleaned_data['model']
            version = form.cleaned_data['version']

            try:
                customer = Customer.objects.get(email=customer_email)
            except Customer.DoesNotExist:
                return JsonResponse({'errors': 'Customer not found'}, status=404)

            order = Order.objects.create(customer=customer, model=model, version=version)

            data = {
                'id': order.id,
                'customer': order.customer.email,
                'robot_model': order.model,
                'robot_version': order.version,
                'fulfilled': order.fulfilled,
            }
            return JsonResponse(data, status=201)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)
