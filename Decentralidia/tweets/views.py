from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Tweet
from .serializer import TweetsSerializer
from rest_framework.renderers import JSONRenderer

class Tweets(APIView):

    def get(self, request):
        print(request.body)
        c = json.loads(request.body.decode('utf-8'))["category"]
        all_entries = Tweet.objects.filter(category=c)
        print(all_entries)
        tweets = []
        for i in range(len(all_entries)):
            serialized_obj = TweetsSerializer(all_entries[0])
            obj = JSONRenderer().render(serialized_obj.data)
            tweets.append(obj)
        return Response({"tweets": tweets}, status=status.HTTP_200_OK)
    

    def post(self, request):
        print(request.body)
        tweet_id = json.loads(request.body.decode('utf-8'))["tweet_id"]
        vote = json.loads(request.body.decode('utf-8'))["vote"]
        tweet = Tweet.objects.filter(id=tweet_id)[0]
        tweet.votes += "#"
        tweet.votes += str(vote)
        print(tweet)
        tweet.save()
        return Response({"status": "successfully"}, status=status.HTTP_200_OK)
