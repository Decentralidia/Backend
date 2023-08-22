from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Tweet
from user.models import User as UserModel
from .serializer import TweetsSerializer
from rest_framework.renderers import JSONRenderer
from django.db.models.functions import Length
from django.db.models import Q
import csv
import io


class Tweets(APIView):

    def get(self, request):
        # print(request.body)
        print(request.GET.get('category', ''))
        c = request.GET.get('category', '')
        fullname = request.GET.get('fullname', '')

        user = UserModel.objects.filter(fullname=fullname)
        if len(user) == 0:
            u = UserModel(fullname=fullname)
            u.save()

        user_votes = UserModel.objects.filter(fullname=fullname)[0].votes.split("#")
        voted_tweets = []
        for vote in user_votes:
            voted_tweets.append(vote.split(":")[0])

        all_entries = Tweet.objects.filter(category=c, enable=True).order_by(Length('votes').asc())
        selected_entries = []
        for tweet in all_entries:
            if len(selected_entries) == 15:
                break
            if str(tweet.id) not in voted_tweets:
                selected_entries.append(tweet)
        all_entries = Tweet.objects.filter(~Q(category=c), enable=True).order_by(Length('votes').asc())
        for tweet in all_entries:
            if len(selected_entries) == 20:
                break
            if str(tweet.id) not in voted_tweets:
                selected_entries.append(tweet)
        all_entries = selected_entries
        print(all_entries)
        tweets = []
        for i in range(len(all_entries)):
            serialized_obj = TweetsSerializer(all_entries[i])
            obj = JSONRenderer().render(serialized_obj.data)
            tweets.append(obj)
        return Response({"tweets": tweets}, status=status.HTTP_200_OK)
    

    def post(self, request):
        print(request.body)
        tweet_id = json.loads(request.body.decode('utf-8'))["tweet_id"]
        vote = json.loads(request.body.decode('utf-8'))["vote"]
        fullname = json.loads(request.body.decode('utf-8'))["fullname"]

        user_votes = UserModel.objects.filter(fullname=fullname)[0].votes
        UserModel.objects.filter(fullname=fullname).update(votes= user_votes + str(tweet_id) + ":" + str(vote) + "#")

        tweet = Tweet.objects.filter(id=tweet_id)[0]
        tweet.votes += "#"
        tweet.votes += str(vote)
        print(tweet)
        tweet.save()
        return Response({"status": "successfully"}, status=status.HTTP_200_OK)

    def put(self, request):
        file_obj = request.FILES['file']
        decoded_file = file_obj.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        spamreader = csv.reader(io_string, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(row)
            t = Tweet(text=row[0].split(',')[1], category=row[0].split(',')[0])
            t.save()
        return Response({"status": "successfully added!"}, status=status.HTTP_200_OK)
