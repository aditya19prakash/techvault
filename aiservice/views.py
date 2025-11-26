from rest_framework.decorators import api_view
from resources.models import Resource
from .ai_summarizer import ask_question
from rest_framework.response import Response
from rest_framework import status
from .models import Ai_saved_answer
@api_view(["POST","GET"])
def ask_ques(request,id):
    if request.method == "GET":
        resource = Resource.objects.get(id=id)
        try:
           result = Ai_saved_answer.objects.filter(resource=resource)
        except Ai_saved_answer.DoesNotExist:
            return Response({resource.title:"THIS resource question is not asked"},status=status.HTTP_404_NOT_FOUND)
        temp = dict()
        for i in result:
            temp[i.question] = i.answer
        return Response(temp,status=status.HTTP_200_OK)
    if not "question" in  request.data:
        return Response({"question":"this field is missing"},status=status.HTTP_404_NOT_FOUND)
    try:
        resource = Resource.objects.get(id=id)
    except:
        return Response({"resource_not_found":"error"})
    if request.method == "POST":
        try:
           result = Ai_saved_answer.objects.get(resource=resource,question =request.data["question"])
           if result is not None:
            return Response({request.data["question"]:result.answer},status=status.HTTP_200_OK)
        except:
            pass
        result = ask_question(request.data["question"],id)    
        Ai_saved_answer.objects.create(resource=resource,question=request.data["question"],answer = result)
        return Response({request.data["question"]:result},status=status.HTTP_200_OK)
    return Response({"error":"error"},status=status.HTTP_404_NOT_FOUND)


