from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from django.db.models import Q
from .models import Like, Post, Repeat
from users.models import User
from .serializers import (
    PostSerializer, LikeSerializer, AllPostSerializer, RepeatSerializer
)

# Create your views here.
class CreatePostAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    def create(self, request):
        serializer_context = {
            'id_user': request.user,
            'request': request,
            'agent': request.META['HTTP_USER_AGENT']
        }

        serializer_data = request.data.get('post', {})
        serializer = self.serializer_class(data=serializer_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def post(self, request):
        id_post = request.data.get('id_post', None)

        try:
            post = Post.objects.get(pk=id_post)
        except Post.DoesNotExist:
            raise NotFound('No se ha encontrado el post')


        if Like.objects.filter(Q(id_user=request.user) & Q(id_post=post)).exists():
            raise NotFound('El like ya existe')
            

        serializer_context = {
            'user': request.user,
            'post': post
        }

        serializer = self.serializer_class(data={}, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Like guardado'})
    
    def delete(self, request):
        id_post = request.data.get('id_post', None)

        try:
            post = Post.objects.get(pk=id_post)
        except Post.DoesNotExist:
            raise NotFound('No se ha encontrado el post')

        try:
            like = Like.objects.get(Q(id_user=request.user) & Q(id_post=post))
        except Like.DoesNotExist:
            raise NotFound('El like no existe')

        like.delete()

        return Response({'message': 'Like borrado'})
    
class PostAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AllPostSerializer

    def get(self, request):

        serializer = self.serializer_class(context=request.user)

        return Response(serializer.get_all_posts())

    def post(self, request):

        serialize_context = {
            'user': request.user,
            'id_post': request.data.get('id_post', None)
        }

        serializer = self.serializer_class(context=serialize_context)

        return Response(serializer.get_post())

class UserPostAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AllPostSerializer

    def post(self, request):

        username = request.data.get('user', None)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('El usuario no existe')

        serialize_context = {
            'user': user,
            'act_user': request.user
        }

        serializer = self.serializer_class(context=serialize_context)

        return Response(serializer.get_user_posts())



class CreateRepeatAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RepeatSerializer

    def post(self, request):
        id_post = request.data.get('id_post', None)

        try:
            post = Post.objects.get(pk=id_post)
        except Post.DoesNotExist:
            raise NotFound('No se ha encontrado el post')


        if Repeat.objects.filter(Q(id_user=request.user) & Q(id_post=post)).exists():
            raise NotFound('El repeat ya existe')
            

        serializer_context = {
            'user': request.user,
            'post': post
        }

        serializer = self.serializer_class(data={}, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Repeat guardado'})

    def delete(self, request):
        id_post = request.data.get('id_post', None)

        try:
            post = Post.objects.get(pk=id_post)
        except Post.DoesNotExist:
            raise NotFound('No se ha encontrado el post')

        try:
            repeat = Repeat.objects.get(Q(id_user=request.user) & Q(id_post=post))
        except Repeat.DoesNotExist:
            raise NotFound('El repeat no existe')

        repeat.delete()

        return Response({'message': 'Repeat borrado'})