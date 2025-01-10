from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
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
@api_view(['POST'])
def loginUser(request):
    body=json.loads(request.body)
    try:
        user=User.objects.get(email=body['email'])
        if not user:
            print(user)
            return Response({"message":"Invalid email and password combination"},status=401)
        refresh = RefreshToken.for_user(user)
        print(refresh)
        response = Response({"message": "Login successful"})
        # Store access token in cookies
        response.set_cookie('access', str(refresh.access_token), httponly=True, samesite='Lax')
        response.set_cookie('refresh', str(refresh), httponly=True, samesite='Lax')
        return response
    except Exception as e:
        print(e)
        return Response({"message":"Internal server error"},status=500)
    
@csrf_exempt
@api_view(['GET'])
def logoutUser(request):
    response=Response({"message":"Logout sucsessfully :)"})
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    return response

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