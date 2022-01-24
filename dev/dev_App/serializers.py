from turtle import mode
from rest_framework import serializers
from dev_App.models import *
from django.shortcuts import get_object_or_404
from django.db import IntegrityError




class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    amount_of_upvotes = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        review = Post.objects.create(**validated_data)
        return review

    def to_representation(self, instance):
        representation = super(PostSerializer, self).to_representation(instance)
        return representation


class VoteSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField()

    def create(self, validated_data):
        post = get_object_or_404(Post, title=validated_data["post_title"])
        vote = Vote()
        vote.post = post
        try:
            vote.save(commit=False)
        except IntegrityError:
            return vote
        return vote


    class Meta:
        model = Vote
        fields = '__all__'


    
