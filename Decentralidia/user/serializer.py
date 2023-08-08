from rest_framework import serializers

class UsersSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    fullname = serializers.CharField(max_length=200)
    votes = serializers.CharField(max_length=300)