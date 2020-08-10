from rest_framework import viewsets, mixins
# Mixins are to override the default viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


# TO reduce code repeating we write this base viewset.
# From where we will inherite our tags, ingredient viewsets
class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    '''Base viewset for user owned recipe attributes like, tags, ingredients'''
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        '''return objects for the current authenticated user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''Create a new tag'''
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    '''Manage tags in the database'''
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    '''Manage ingridients in the database'''
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewset(viewsets.ModelViewSet):
    '''Manage recipes in the database'''
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        '''return objects for the current authenticated user only'''
        return self.queryset.filter(user=self.request.user)
