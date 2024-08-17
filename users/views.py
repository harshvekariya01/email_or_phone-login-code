import re
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import  login
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from .serializers import *
from .models import *


class UserView(ModelViewSet):
    permission_classes = (permissions.AllowAny,)

    def create_user_api(self, request):
        data = request.data
        email, phone = None, None
        email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        phone_regex = r'^\d{10}$'
        if re.match(email_regex, data.get('email_phone')):
            email = data.get('email_phone')
        elif re.match(phone_regex, data.get('email_phone')):
            phone = data.get('email_phone')
        else:
            return Response({'message': 'Invalid email or phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        if email and User.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if phone and User.objects.filter(phone_number=phone).exists():
            return Response({'message': 'Phone already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user_obj = User.objects.create(name=str(data.get('name')),
                                       email=email,
                                       phone_number=phone,
                                       password=make_password(data.get('password')),
                                       )
        if user_obj:
            return Response({'data': 'User Created Successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'somthing went wrong'}, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        
        response = super(UserLoginView, self).post(request, *args, **kwargs)
        response.data['id'] = user.id
        response.data['email'] = user.email
        response.data['name'] = user.name
        
        return Response({'status': True, 'data': response.data}, status=status.HTTP_200_OK)