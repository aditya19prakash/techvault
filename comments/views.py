from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Comment
from users.models import User
from resources.models import Resource
from .serializers import CommentsPOSTSerializer,CommentsGETSerializer
from votes.models import Comments_votes
@api_view(["GET","POST"])
def comments(request,id):
    resource = Resource.objects.get(id = id)
    if request.method == "GET":
        comment = Comment.objects.filter(resource=resource,parent = None)
        result = []
        for cme in comment:
            serializer = CommentsGETSerializer(cme).data
            serializer["user_name"] = cme.user.username
            vote = None 
            try:
                vote = Comments_votes.objects.get(comments=cme)
            except:
                pass
            up_vote =0
            down_vote =0
            if not vote is None:
                for i in vote:
                    if i.vote == "upvote":
                        up_vote+=1
                    else:
                        down_vote+=1
            serializer["up_vote"] = up_vote
            serializer["down_vote"] = down_vote
            result.append(serializer)
        return Response(result, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        serializer = CommentsPOSTSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(resource=resource)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    return Response({"error":"error"},status=status.HTTP_404_NOT_FOUND)
@api_view(["GET","POST"])
def nested_comments(request,id,cmt_id):
    resource = Resource.objects.get(id = id)
    comment = Comment.objects.get(id = cmt_id)
   
    if request.method == "GET":
       
        nested_comment = Comment.objects.filter(parent = comment)
        result = []
        for cme in nested_comment:
            serializer = CommentsGETSerializer(cme).data
            serializer["user_name"] = cme.user.username
            vote = None 
            try:
                vote = Comments_votes.objects.get(comments=cme)
            except:
                pass
            up_vote =0
            down_vote =0
            if not vote is None:
                for i in vote:
                    if i.vote == "upvote":
                        up_vote+=1
                    else:
                        down_vote+=1
            serializer["up_vote"] = up_vote
            serializer["down_vote"] = down_vote
            result.append(serializer)
        return Response(result, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        serializer = CommentsPOSTSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(resource=resource,parent=comment)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response({"error":"error"},status=status.HTTP_404_NOT_FOUND)
