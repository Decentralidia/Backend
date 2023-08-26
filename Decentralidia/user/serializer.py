from rest_framework import serializers

class UsersSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    fullname = serializers.CharField(max_length=200)
    votes = serializers.CharField(max_length=300)
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=[(tag, tag.value) for tag in GENDER_CHOICES])
    likes_dislikes = serializers.CharField(max_length=100000, required=False)