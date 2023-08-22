from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import  RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import status

@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    __, token = AuthToken.objects.create(user)

    return Response({
        'user_info':{
            'id':user.id,
            'username':user.username,
            'email':user.email 
        },
        'token':token
    })

@api_view(['GET'])
def get_user_data(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'user_info':{
                'id':user.id,
                'username':user.username,
                'email':user.email 
            },
        })
    
    return Response({'error': 'no autenticado'}, status=400)

@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    __, token = AuthToken.objects.create(user)

    return Response({
        'user_info':{
            'id':user.id,
            'username':user.username,
            'email':user.email 
        },
        'token':token
        })



@api_view(['GET'])
def get_list_users(request):
    user = request.user

    if user.is_authenticated == False:
        return Response({'error': 'No Autenticado'}, status.HTTP_401_UNAUTHORIZED)
    
    snippets = User.objects.all()
    serializer = RegisterSerializer(snippets, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

# https://www.django-rest-framework.org/tutorial/2-requests-and-responses/

# class ListUsersView(generics.ListAPIView):
#     serializer_class = RegisterSerializer

#     Response({'error': 'no autenticado'}, status=400)
#     # def get_queryset():
#         # user = self.request.user
        
        
            
#         # return Response({'error': 'no autenticado'}, status=400)
#         # print('hola')