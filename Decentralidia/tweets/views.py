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
        c = request.GET.get('category', '')
        fullname = request.GET.get('fullname', '')
        age = request.GET.get('age')
        gender = request.GET.get('gender')
    
        # Checking if the age is a valid integer
        try:
            age = int(age)
        except ValueError:
            return Response({"error": "Invalid age provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Checking if gender is one of the predefined values
        if gender not in ['male', 'female', 'non-binary', 'other']:
            return Response({"error": "Invalid gender provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Efficiently get or create a user
        user, created = UserModel.objects.get_or_create(
            fullname=fullname, 
            defaults={
                'age': age,
                'gender': gender
            }
        )
    
        # Check the votes for the user and exclude tweets that the user has already voted on
        user_votes = user.votes.split("#")
        voted_tweets = [vote.split(":")[0] for vote in user_votes]
    
        # Retrieve tweets based on the provided category
        all_entries = Tweet.objects.filter(category=c, enable=True).exclude(id__in=voted_tweets).order_by(Length('votes').asc())
        selected_entries = list(all_entries)[:15]
    
        # If we haven't reached 20 tweets yet, get more tweets from other categories
        if len(selected_entries) < 20:
            remaining_count = 20 - len(selected_entries)
            all_entries = Tweet.objects.exclude(category=c).exclude(id__in=voted_tweets).order_by(Length('votes').asc())
            selected_entries += list(all_entries)[:remaining_count]
    
        # Serialize the tweets
        tweets = [JSONRenderer().render(TweetsSerializer(tweet).data) for tweet in selected_entries]
    
        return Response({"tweets": tweets}, status=status.HTTP_200_OK)

    
    def post(self, request):
        tweet_id = json.loads(request.body.decode('utf-8'))["tweet_id"]
        vote = json.loads(request.body.decode('utf-8'))["vote"]
        fullname = json.loads(request.body.decode('utf-8'))["fullname"]
        like_or_dislike = json.loads(request.body.decode('utf-8')).get("like_dislike", None)

        user = UserModel.objects.filter(fullname=fullname).first()
        if not user:
            return Response({"status": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.votes += str(tweet_id) + ":" + str(vote) + "#"
        user.save()

        if like_or_dislike:
            user.likes_dislikes += str(tweet_id) + ":" + like_or_dislike + "#"
            user.save()

            tweet = Tweet.objects.filter(id=tweet_id).first()
            if tweet:
                tweet.likes_dislikes += str(user.id) + ":" + like_or_dislike + "#"
                tweet.save()
            else:
                return Response({"status": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)

        tweet = Tweet.objects.filter(id=tweet_id).first()
        if tweet:
            tweet.votes += "#" + str(vote)
            tweet.save()
        else:
            return Response({"status": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)

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
