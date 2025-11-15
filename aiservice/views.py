from rest_framework.decorators import api_view
from .ai_summarizer import ask_question
from rest_framework.response import Response
from rest_framework import status
from .models import Ai_saved_answer
@api_view(["POST"])
def ask_ques(request,id):
    if not "question" in  request.data:
        return Response({"question":"this field is missing"},status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        try:
           result = Ai_saved_answer.objects.get(question =request.data["question"] )
           if result is not None:
            return Response({request.data["question"]:result.answer},status=status.HTTP_200_OK)
        except:
            pass
        result = ask_question(request.data["question"],id)
        Ai_saved_answer.objects.create(question=request.data["question"],answer = result)
        return Response({request.data["question"]:result},status=status.HTTP_200_OK)
    return Response({"error":"error"},status=status.HTTP_404_NOT_FOUND)