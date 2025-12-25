from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import  User
from .models import Comment
from resources.models import Resource
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentsPOSTSerializer,CommentsGETSerializer
from votes.models import Comments_votes
from votes.serializers import Comments_votes_Serializers
from  concurrent.futures import ThreadPoolExecutor
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
class CommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        cache_key = f"comment_view:{request.get_full_path()}"
        cache_response = cache.get(cache_key)
        if cache_response:
            return Response(cache_response,status=200)
        resource = Resource.objects.get(id=id)
        comments = Comment.objects.filter(resource=resource, parent=None).select_related('user').prefetch_related("replies")
        result = []
        def comment_list(cme):
            serializer = CommentsGETSerializer(cme).data
            serializer["user_name"] = cme.user.username
            nested_count = len(cme.replies.all())
            serializer["nested_comments"] = nested_count
            votes = Comments_votes.objects.filter(comments=cme)
            up_vote = votes.filter(vote="upvote").count()
            down_vote = votes.filter(vote="downvote").count()
            serializer["up_vote"] = up_vote
            serializer["down_vote"] = down_vote
            return serializer
        with ThreadPoolExecutor(max_workers=20) as threads:
           result = list(threads.map(comment_list,comments))
        cache.set(cache_key,result,timeout=60*60)
        return Response(result, status=status.HTTP_200_OK)
    
    def put(self,request):
        try:
            comments_id = request.data["comment_id"]
            user = User.objects.get(id=request.data["user"])
            vote_value = request.data["votes"].lower()
            comments = Comment.objects.get(id=comments_id)
            if vote_value not in ["upvote", "downvote"]:
                return Response({"message": "Invalid vote type"}, status=status.HTTP_400_BAD_REQUEST)
            comment_obj, created = Comments_votes.objects.get_or_create(
                user=user,
                comments=comments
            )
            comment_obj.vote = vote_value
            comment_obj.save()
            serializer = Comments_votes_Serializers(comment_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"Not_found": "USER_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,id):
        data = request.data.copy()
        data["user"] = request.user.id
        data["resource"] = id
        serializer = CommentsPOSTSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NestedComments(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id,cmt_id):
        cache_key = f"NestedComments_view:{request.get_full_path()}"
        cache_response = cache.get(cache_key)
        if cache_response:
            return Response(cache_response,status=200)
        nested_comment = Comment.objects.filter(parent_id=cmt_id)
        result = []
        def nested_comments(cme):
            serializer = CommentsGETSerializer(cme).data
            serializer["user_name"] = cme.user.username
            vote = None 
            try:
                vote = Comments_votes.objects.filter(comments=cme)
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
            return serializer
        with ThreadPoolExecutor(max_workers=20) as threads:
           result = list(threads.map(nested_comments,nested_comment))
        cache.set(cache_key,result,timeout=60*60)
        return Response(result, status=status.HTTP_200_OK)
    

    def post(self,request,id,cmt_id):
        resource = Resource.objects.get(id =id)
        serializer = CommentsPOSTSerializer(data=request.data)
        comment = Comment.objects.get(id = cmt_id)
        if serializer.is_valid():
            serializer.save(resource=resource,parent=comment)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
