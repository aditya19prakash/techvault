from rest_framework.response import Response
from rest_framework import status
from resources.models import Resource
from aiservice.models import Ai_summary
from votes.models import Resource_votes
from comments.models import Comment
from aiservice.ai_summarizer import ai_summarizer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from aiservice.models import Ai_summary
from resources.serializers import (
  ResourcePUTSerializerID, ResourcePostSerializer, 
  ResourceViewSerializer, ResourceViewSerializerID )
import concurrent.futures


class ResourcePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 50

class ResourceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cache_key = f"resource_view:{request.get_full_path()}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        resources = Resource.objects.all().order_by("-views")
        paginator = ResourcePagination()
        page = paginator.paginate_queryset(resources, request) or []

        def extract_voting(res):
            up_vote = 0
            down_vote = 0

            comments_count = Comment.objects.filter(
                resource=res, parent=None
            ).count()

            for v in Resource_votes.objects.filter(resource=res):
                if v.vote == "upvote":
                    up_vote += 1
                else:
                    down_vote += 1

            res_data = ResourceViewSerializer(res).data
            res_data["up_vote"] = up_vote
            res_data["down_vote"] = down_vote
            res_data["comments"] = comments_count
            return res_data

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            result = list(executor.map(extract_voting, page))

        paginated_data = paginator.get_paginated_response(result).data
        cache.set(cache_key, paginated_data, timeout=60)

        return Response(paginated_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        if "tech_stack" in data:
            techs = data["tech_stack"].split(",")
            unique_techs = []
            for t in techs:
                if t not in unique_techs:
                    unique_techs.append(t)
            data["tech_stack"] = ",".join(unique_techs)

        serializer = ResourcePostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
class ResourceViewId(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  def get(self,request,id):
    try:
        cache_key = f"resource_view_id:{request.get_full_path()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        resource = Resource.objects.get(id=id)
        serializers = ResourceViewSerializerID(resource)
        resource.views+=1
        resource.save(update_fields=['views'])
        data = serializers.data
        comments = Comment.objects.filter(resource_id=id).count()
        up_vote = 0
        down_vote = 0
        vote = Resource_votes.objects.filter(resource=resource)
        for v in vote:
          if v.vote == "upvote": 
            up_vote+=1
          else:
            down_vote+=1
        ai_summary = None
        try:
          ai_summary = Ai_summary.objects.get(resource=resource)
        except Ai_summary.DoesNotExist:
           pass
        if ai_summary is None:
           ai_summary = Ai_summary.objects.create(resource=resource,summary = ai_summarizer(resource.url))
        data["up_vote"] = up_vote
        data["down_vote"]=down_vote
        data["comments"]=comments
        data["ai_summary"] =ai_summary.summary
        cache.set(cache_key,data,timeout=60*60)
        return Response(data, status=status.HTTP_200_OK)
    except Resource.DoesNotExist:
        return Response({"message":"NOT FOUND"},status=status.HTTP_404_NOT_FOUND) 
  
  def put(self,request,id):
    try:  
      resource = Resource.objects.get(id=id,user=request.user)
      url = request.data.get("url")
      if url and url != resource.url:
         Ai_summary.objects.filter(resource_id=id).delete()
      
      serializers = ResourcePUTSerializerID(resource,data=request.data,partial=True)
      if serializers.is_valid():
        updated_resource = serializers.save()
        view_serializer = ResourceViewSerializerID( updated_resource )
        return Response(view_serializer.data,status=status.HTTP_200_OK)
    except:
       return Response({"message":"updation is failed"},status=400)

class ResourceVoting(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  def post(self,request,id):
      vote = request.data.get("vote")
      try:
         res = Resource.objects.get(id=id)
      except Resource.DoesNotExist:
         return Response({"message":"resource not found"},status=404)
      if not vote :
         return Response({"meesage":"vote is not given"},status=400)
      def save_vote(vote):
          resource_vote = Resource_votes.objects.filter(resource=res,user=request.user).first()
          vote=vote.lower()
          if resource_vote is None:
            Resource_votes.objects.create(user= request.user,resource=res,vote=vote)
          else:
            resource_vote.vote = vote
            resource_vote.save(update_fields=["vote"])
      if vote.lower() == "upvote":
         save_vote("upvote")
      elif vote.lower() == "downvote":
         save_vote("downvote")
      else:
         return Response({"message":"votes is not in given format give upvotes or downvotes "},status=400)
      return Response({"message":"Success votes is registered"},status=200)
      
class TechstackView(APIView):
  def get(self,request):
    cache_key = f"resource_view:{request.get_full_path()}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data, status=status.HTTP_200_OK)
    resource = Resource.objects.all()
    tech_groups = dict()
    for obj in resource:
      techs = list(obj.tech_stack.split(","))
      for i in techs:
        i = i.strip()
        if i in tech_groups:
          tech_groups[i]+= 1
        else:
          tech_groups[i]= 1
    cache.set(cache_key,tech_groups,timeout=60*60)
    return Response(tech_groups,status=status.HTTP_200_OK)