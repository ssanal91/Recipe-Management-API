from rest_framework import serializers
from Recipe.models import recipe
from Recipe.models import review
from django.contrib.auth.models import User

class RecipeSerializers(serializers.ModelSerializer):
    class Meta:
        model=recipe
        fields=['id','recipe_name','recipe_ingredients','instruction','cuisine','meal_type']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'],
                                       password=validated_data['password'])
        user.save()
        return user

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model=review
        fields='__all__'