from rest_framework.viewsets  import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from activities.models import ActivityItem, ActivityList
from activities.serializers import ActivityListSerializer
from rest_framework.response import Response
from rest_framework import status



class ActivityListViewSet(ModelViewSet):
    queryset = ActivityList.objects.all()
    serializer_class = ActivityListSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    
    

    # def create(self, validated_data):
    #     username = validated_data.get('username')
    #     password = validated_data.get('password')
    #     email = validated_data.get('email')
    #     first_name = validated_data.get('first_name')
    #     last_name = validated_data.get('last_name')

    #     user = User.objects.create(
    #         username = username,
    #         password = password,
    #         first_name = first_name,
    #         last_name = last_name,
    #         email = email
    #     )

    #     return user
        