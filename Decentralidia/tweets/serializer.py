from rest_framework import serializers

class TweetsSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    text = serializers.CharField(max_length=200)
    category = serializers.CharField(max_length=200)
    votes = serializers.CharField(max_length=200)