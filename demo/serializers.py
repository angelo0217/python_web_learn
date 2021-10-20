from rest_framework import serializers
from demo.models import Demo

class DemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demo
        #fielsd = '__all__'
        fields = ('name', 'age')