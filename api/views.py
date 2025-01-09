from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
# Create your views here.
@csrf_exempt
def getUsers(request):
    if request.method=="GET":
        users=list(User.objects.all().values())
        return JsonResponse(users,safe=False)
    return HttpResponse(status=405)
@csrf_exempt
def createUser(request):
    body=json.loads(request.body)
    if request.method=="POST":
        User.objects.create(
            age=body['age'],
            name=body['name'],
            email=body['email']
        )
        return JsonResponse({"message":"created sucessfully :)"},status=200)
    return JsonResponse(status=500)

@csrf_exempt
def deleteUser(request,userId):
    if request.method=='DELETE':
        try:
            user=User.objects.get(id=userId)
            user.delete()
            return JsonResponse({"message":"user deleted sucessfully :)"},status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)
    return HttpResponse(status=405)
@csrf_exempt
def updateUser(request,userId):
    body=json.loads(request.body)
    if request.method=="PUT":
        try:
            user=User.objects.get(id=userId)
            user.name=body['name']
            user.age=body['age']
            user.email=body['email']
            user.save()
            return JsonResponse({"message":"user update sucessfully :)"},status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)
    return HttpResponse(status=405)