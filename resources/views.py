from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Resource
from aiservice.models import Ai_summary
from .serializers import *
from votes.models import Votes
from comments.models import Comment
from aiservice.ai_summarizer import ai_summarizer
@api_view(["GET","POST"])
def resource_view(request):
  if request.method=='GET':
    resource = Resource.objects.all().order_by('-views')
    result =[]
    for res in resource:
      up_vote =0
      down_vote =0
      comments_count = None
      try:
        pass
        comments_count=len(Comment.objects.filter(resource=res,parent=None))
      except:
        pass
      vote = Votes.objects.filter(resource=res)
      for v in vote:
        if v.vote == "upvote": 
          up_vote+=1
        else:
          down_vote+=1
      res_data = ResourceViewSerializer(res).data
      res_data["up_vote"] = up_vote
      res_data["down_vote"] = down_vote
      res_data["comments"]=comments_count
      result.append(res_data)
    return Response(result, status=status.HTTP_200_OK)
  if request.method=='POST':
    serializer =ResourcePostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
 
@api_view(["GET","PUT"])
def resource_view_id(request,id):
  try:
   resource = Resource.objects.get(id=id)
  except:
    return Response({"message":"NOT FOUND"},status=status.HTTP_404_NOT_FOUND) 
  if request.method=='GET':
    serializers = ResourceViewSerializerID(resource)
    resource.views+=1
    resource.save(update_fields=['views'])
    data = serializers.data
    up_vote = 0
    down_vote = 0
    vote = Votes.objects.filter(resource=resource)
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
    data["Votes_message"]="you want to votes then send "
    data["ai_summary"] =ai_summary.summary
    return Response(data, status=status.HTTP_200_OK)
  

  elif request.method=='PUT':
    if "votes" in request.data and "user" in request.data:
      try:
        user = User.objects.get(id=request.data["user"])
        resource = Resource.objects.get(id=id)
        vote_value = request.data["votes"].lower()

        if vote_value not in ["upvote", "downvote"]:
            return Response({"message": "Invalid vote type"}, status=status.HTTP_400_BAD_REQUEST)
        vote_obj, created = Votes.objects.get_or_create(user=user, resource=resource)
        vote_obj.vote = vote_value
        vote_obj.save()
        serializer = ResourceViewSerializerID(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)

      except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
      except Resource.DoesNotExist:
        return Response({"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
      serializers = ResourcePUTSerializerID(resource,data=request.data)
      if serializers.is_valid():
        updated_resource = serializers.save()
        view_serializer = ResourceViewSerializerID( updated_resource )
        return Response(view_serializer.data,status=status.HTTP_200_OK)
  return Response(status=status.HTTP_404_NOT_FOUND)




@api_view(["GET"])  
def techstack_view(request):
   if request.method == "GET":
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
    return Response(tech_groups,status=status.HTTP_200_OK)
   




       
       
