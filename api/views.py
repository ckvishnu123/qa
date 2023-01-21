from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework.decorators import action

from api.serializers import UserSerializer, QuestionSerializer, AnswerSerializer
from api.models import Questions, Answers

# Create your views here.

class UsersView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # using http method names we can set whatever method is needed
    http_method_names = ["post"]

class QuestionsView(ModelViewSet):
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = QuestionSerializer
    queryset =  Questions.objects.all()

    # overwriting perform create as we need to pass user also
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_questions(self, request, *ar, **kw):
        qs = Questions.objects.filter(user=request.user)
        serializer = QuestionSerializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=True, methods=['post'])
    def add_answer(self, request, *ar, **kw):
        """ id = kw.get("pk")
        qstn = Questions.objects.get(id=id)
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            qstn.answers_set.create(**serializer.validated_data, user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors) """

        # above code is correct also(mine :)), anyone can be used

        id = kw.get("pk")
        qstn = Questions.objects.get(id=id)
        usr = request.user
        serializer = AnswerSerializer(data=request.data, context={"user": usr,
        "question": qstn})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(detail=True, methods=["get"])
    def list_answers(self, request, *ar, **kw):
        id = kw.get("pk")
        ques = Questions.objects.get(id=id)
        qs = ques.answers_set.all()
        serializer = AnswerSerializer(qs, many=True)
        return Response(data=serializer.data)


class AnswersView(ModelViewSet):
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = AnswerSerializer
    queryset = Answers.objects.all()
    http_method_names = ["get"]

    @action(detail=True, methods=["get"])
    def up_vote(self, request, *ar, **kw):
        """ id = kw.get("pk")
        ans = Answers.objects.get(id=id) """
        # instead we can also use 
        ans = self.get_object()
        ans.up_vote.add(request.user)
        return Response(data="success")