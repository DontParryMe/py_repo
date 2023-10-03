import json
from django.http import JsonResponse
from .forms import RobotForm


def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = RobotForm(data)
            if form.is_valid():
                form.save()
                response_data = {
                    'message': 'Robot record created successfully.'
                }
                return JsonResponse(response_data, status=201)
            else:
                response_data = {
                    'error': 'Invalid data. Please check your input.'
                }
                return JsonResponse(response_data, status=400)
        except json.JSONDecodeError:
            response_data = {
                'error': 'Invalid JSON data.'
            }
            return JsonResponse(response_data, status=400)
    else:
        response_data = {
            'error': 'Invalid request method.'
        }
        return JsonResponse(response_data, status=400)
