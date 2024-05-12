from django.shortcuts import render
from rest_framework.decorators import api_view
from Recipe.models import recipe,review
from Recipe.serializers import RecipeSerializers,UserSerializer,ReviewSerializers
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

@api_view(['GET','POST'])
def allrecipe(request):
    if(request.method=="GET"):
        r=recipe.objects.all()
        rp=RecipeSerializers(r,many=True)
        return Response(rp.data)
    elif(request.method=="POST"):
        rp=RecipeSerializers(data=request.data)
        if rp.is_valid():
            rp.save()
            return Response(rp.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['GET','PUT','DELETE'])
def recipedetails(request,pk):
        try:
            r=recipe.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (request.method == "GET"):
            rp=RecipeSerializers(r)
            return Response(rp.data)
        elif(request.method=="PUT"):
            rp=RecipeSerializers(r,data=request.data)
            if rp.is_valid():
                rp.save()
                return Response(rp.data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif(request.method=="DELETE"):
            r.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
# @api_view(['POST',])
# def register(request):
#      if(request.method=="POST"):
#          reg=UserSerializer(data=request.data)
#          if reg.is_valid():
#              reg.save()
#              return Response(reg.data,status=status.HTTP_201_CREATED)
#          return Response(status=status.HTTP_400_BAD_REQUEST)

class UserViewset(viewsets.ModelViewSet): #For registration
    queryset=User.objects.all()
    serializer_class=UserSerializer

class createreview(viewsets.ModelViewSet):
    queryset = review.objects.all()
    serializer_class = ReviewSerializers
class retrievereview(APIView):
    def get_object(self,pk):
        try:
            return recipe.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
    def get(self,request,pk):
        k=self.get_object(pk)
        sr=review.objects.filter(recipe_name=k)
        ser=ReviewSerializers(sr,many=True)
        return Response(ser.data)


class Cuisinefilter(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        query=self.request.query_params.get('cuisine')
        R=recipe.objects.filter(cuisine=query)
        res=RecipeSerializers(R,many=True)
        return Response(res.data)

class mealfilter(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        query=self.request.query_params.get('meal')
        R=recipe.objects.filter(meal_type=query)
        res=RecipeSerializers(R,many=True)
        return Response(res.data)

class ingredientfilter(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        query=self.request.query_params.get('ing')
        R=recipe.objects.filter(recipe_ingredients=query)
        res=RecipeSerializers(R,many=True)
        return Response(res.data)

class user_logout(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self,request):
        self.request.user.auth_token.delete()
        return Response({'msg':"Logout Successfully"},status=status.HTTP_200_OK)


class Detailrev(APIView):
    permission_classes = [IsAuthenticated,]
    def get_object(self,pk):
        try:
            return recipe.objects.get(pk=pk)
        except:
            return Http404
    def get(self,request,pk):
        r=self.get_object(pk)
        rev=review.objects.filter(recipe_name=r)






