from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from users.models import User
from .models import Comment
from resources.models import Resource
from .serializers import CommentsPOSTSerializer,CommentsGETSerializer
from votes.models import Comments_votes
from votes.serializers import Comments_votes_Serializers
@api_view(["GET","POST"])
def comments(request, id):
    resource = Resource.objects.get(id=id)

    if request.method == "GET":
        comments = Comment.objects.filter(resource=resource, parent=None).select_related('user').prefetch_related('replies')
        result = []
        for cme in comments:
            serializer = CommentsGETSerializer(cme).data
            serializer["user_name"] = cme.user.username
            nested_count = len(cme.replies.all())
            serializer["nested_comments"] = nested_count
            votes = Comments_votes.objects.filter(comments=cme)
            up_vote = votes.filter(vote="upvote").count()
            down_vote = votes.filter(vote="downvote").count()
            serializer["up_vote"] = up_vote
            serializer["down_vote"] = down_vote
            result.append(serializer)
        return Response(result, status=status.HTTP_200_OK)
    
    if request.method == "POST" and "votes" in request.data and "user" in request.data:
            serializer
            try:
                user = User.objects.get(id=request.data["user"])
                vote_value = request.data["votes"].lower()
                comments = Comment.objects.get(id=id)
                if vote_value not in ["upvote", "downvote"]:
                    return Response({"message": "Invalid vote type"}, status=status.HTTP_400_BAD_REQUEST)
                comment,created = Comments_votes.objects.get_or_create(user=user,comments=comments)
                comment.vote = vote_value
                comment.save()
                serializer = Comments_votes_Serializers(comment)
            except User.DoesNotExist:
                return Response({"Not_found":"USER_NOT_FOUND"},status = status.HTTP_404_NOT_FOUND) 
            except:
                return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
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
