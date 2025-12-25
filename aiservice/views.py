from rest_framework.permissions import IsAuthenticated
from resources.models import Resource
from .ai_summarizer import ask_question
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Ai_saved_answer
class AskQuesView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if not "question" in  request.data:
            return Response({"question":"this field is missing"},status=status.HTTP_404_NOT_FOUND)
        try:
            resource = Resource.objects.get(id= request.user.id)
        except:
            return Response({"resource_not_found":"error"})
        if request.method == "POST":
            try:
               result = Ai_saved_answer.objects.get(resource=resource,question =request.data["question"])
               if result is not None:
                return Response({request.data["question"]:result.answer},status=status.HTTP_200_OK)
            except:
                pass
            result = ask_question(request.data["question"],request.user.id)    
            Ai_saved_answer.objects.create(resource=resource,question=request.data["question"],answer = result)
            return Response({request.data["question"]:result},status=status.HTTP_200_OK)
        return Response({"error":"error"},status=status.HTTP_404_NOT_FOUND)


