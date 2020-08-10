from rest_framework import serializers
from .models import Post, Vote


# we use serializer to show/get data to/from api as our model and json format
class PostSerializer(serializers.ModelSerializer):
    # here we are giving this fields readonly mode
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')

    # to show all the votes this post belongs to
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created', 'votes']

    def get_votes(self, post):
        # function name pattern get_fieldname, to return all votes this post belongs to
        return Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']
