from rest_framework import generics, status, viewsets
from .models import *
from .serializers import *
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CastVoteView(APIView):

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            created_instance = serializer.create(validated_data=request.data)

            try:
                created_instance.save()

            except IntegrityError:
                return Response(
                    {
                        "message": "Already voted"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "message": "Vote cast successful"
                },
                status=status.HTTP_200_OK
            )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer