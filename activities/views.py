from rest_framework.viewsets  import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from activities.models import ActivityItem, ActivityList
from activities.serializers import ActivityItemSerializer, ActivityListDetailSerializer, ActivityListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ActivityListDetailSerializer
        return self.serializer_class
    
    @action(detail=True, methods=['get'])
    def finish_list(self, request, pk=None):
        isnstance = self.get_object()
        items = ActivityItem.objects.filter(list_id=isnstance)
        for item in items:
            item.satus = 'FI'
            item.save()
        serializer = self.get_serializer(isnstance)
        return Response(serializer.data)

    

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

class ActivityItemViewSet(ModelViewSet):
    queryset = ActivityItem.objects.all()
    serializer_class = ActivityItemSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    def get_queryset(self):
        filter = {'owner': self.request.user}
        list_id = self.request.query_params.get('list_id', None)
        if list_id is not None:
            filter['list_id_id'] = list_id
        return self.queryset.filter( **filter )