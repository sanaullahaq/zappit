from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from .models import Post, Vote
from rest_framework.response import Response
from .serializers import PostSerializer, VoteSerializer
from rest_framework.exceptions import ValidationError


# we are going to create a class based view
# ListAPIView just view the data as a list, but ListCreateAPIView will let user create data also
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # in a class view we can specify who has the permission to cll the api
    # permissions.IsAuthenticate will not let a anonymous user cll the api
    # permissions.IsAuthenticatedOrReadOnly will let the anonymous user cll the api in readonly mode only
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # function name is constant
    # serializer holds a model
    # before saving something into the db this will be called
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # until above 3 lines are okk to delete a post, but the prob is everyone can delete post of each other,
    # that's why we have gone further, a simpler way to delete a post of his won
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This isn\'t your post to delete, BRUH!')


# no one wants to see the individuals votes, that's why only CreateAPIView what will be created only vote objects
class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post :)')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # it means we has been get rid of it
        else:
            raise ValidationError('You never voted for this post :(')
