import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomerForm
from .models import Customer


@csrf_exempt
def create_customer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = CustomerForm(data=data)  # Используем вашу форму для валидации данных

        if form.is_valid():
            email = form.cleaned_data['email']
            # Проверяем уникальность адреса электронной почты в базе данных
            if Customer.objects.filter(email=email).exists():
                return JsonResponse({'errors': 'Provided email already exists.'}, status=400)
            else:
                customer = Customer(email=email)
                customer.save()
                return JsonResponse({'id': customer.id, 'email': customer.email}, status=201)
        else:
            # Если данные формы неверные, возвращаем ошибку с сообщением об ошибке в форме
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        # Если запрос не методом POST, возвращаем ошибку "Метод не разрешен"
        return JsonResponse({'error': 'Method not allowed'}, status=405)
