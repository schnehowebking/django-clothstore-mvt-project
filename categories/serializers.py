from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Category
        fields = '__all__'
