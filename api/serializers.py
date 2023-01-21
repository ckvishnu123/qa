from rest_framework import serializers
from api.models import Questions, Answers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    # what we pass in request body should add in fields and that should not be a-
    # read only field
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    created_date = serializers.CharField(read_only=True)
    upvote_count = serializers.CharField(read_only=True)
    class Meta:
        model = Answers
        fields = ["id", "answer", "user", "created_date", "upvote_count"]

    def  create(self, validated_data):
        user = self.context.get("user")
        question = self.context.get("question")
        return question.answers_set.create(**validated_data, user=user)


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    question_answers = AnswerSerializer(read_only=True, many=True)
    
    class Meta:
        model = Questions
        fields = ["id", "title", "image", "description", "user", "question_answers"]

