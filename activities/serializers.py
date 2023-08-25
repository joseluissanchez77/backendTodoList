from rest_framework import serializers

from activities.models import ActivityItem, ActivityList

class ActivityListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    status = serializers.ReadOnlyField()
    item_count = serializers.ReadOnlyField()

    class Meta: 
        model = ActivityList
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ActivityListSerializer, self).to_representation(instance)
        representation['created_at'] =  instance.created_at.astimezone().strftime("%Y-%m-%d %H:%M")
        return representation
    
class ActivityItemSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta: 
        model = ActivityItem
        fields = '__all__'
        # fields = ['id','title','description','owner','list_id','status','created_at','updated_at']
    
    def to_representation(self, instance):
        representation = super(ActivityItemSerializer, self).to_representation(instance)
        representation['status'] =  instance.get_status_display()
        return representation
    
    #que solo el usuario se pueda cambiar a la lista q pertence
    def _validate_user(self, validate_data):
        auth_user = self.context['request'].user
        list_id = validate_data.get('list_id')
        activity_list = ActivityList.objects.get(pk=list_id.id)
        if activity_list.owner != auth_user:
            raise serializers.ValidationError('No se encontro una lista asociada al usuario', code='authorization')
        

    def create(self, validated_data):
        #validar que la lista pertenezca a un usaurio q es
        self._validate_user(validated_data)
        return ActivityItem.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        list_id = validated_data.get('list_id', None)
        if list_id:
            self._validate_user(validated_data)
        
        for attr, value in validated_data.items():
            setattr(instance, attr,value)
        instance.save()
        return instance
    

class ActivityListDetailSerializer(serializers.ModelSerializer):
    items = ActivityItemSerializer(many=True, read_only=True)
    status = serializers.ReadOnlyField()
    item_count = serializers.ReadOnlyField()

    class Meta:
        model = ActivityList
        fields = ['id', 'status','title', 'items','description','item_count', 'created_at', 'updated_at']

