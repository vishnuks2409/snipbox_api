from django.shortcuts import render
from rest_framework import  generics
from rest_framework.permissions import IsAuthenticated
from .models import Snippet,Tags
from .serializers import SnippetSerializers,TagSerializers,UserSerializer
from django.contrib.auth.models import User
from  rest_framework.response import Response
from rest_framework.views import  APIView
from django.http import Http404


# Create your views here.

""" The view is used to Register new user """
class Register(generics.ListCreateAPIView):
    queryset =User.objects.all()
    serializer_class = UserSerializer


"""snippet_create view is used to craete a new snippet
   authenticated user have only access to add new snippet """
class Snippet_create(generics.CreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


""" This view is used to detailview of snippet by the current user and 
    update the existing snippet """
class SnippetDetail(generics.RetrieveUpdateAPIView):
    queryset = Snippet.objects.filter()
    serializer_class = SnippetSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


""" The view Return total number of snippets and 
     list of available snippets with a hyperlink to respective detail APIs"""

class SnippetOverview(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        snippets = Snippet.objects.all()
        total_count = snippets.count()
        snippet_list = SnippetSerializers(snippets, many=True, context={'request': request}).data
        return Response({
            'total_count': total_count,
            'snippets': snippet_list
        })


"""delete a particular snippets and return the list of available snippets"""
class DeleteSnippet(APIView):
    def get_object(self,pk):
        """ getting the snippets by id"""
        try:
            return Snippet.objects.get(pk=pk)
        except:
            raise Http404

    def delete(self, request, pk):
        b=self.get_object(pk)
        b.delete()
        available= Snippet.objects.all()
        available_snippet=SnippetSerializers(available,many=True)
        return Response(available_snippet.data)

""" show all the available tags in the database"""
class TagList(generics.ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializers
    permission_classes = [IsAuthenticated]


"""show the snippets available by a particular tag"""
class TagDetail(generics.RetrieveAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializers
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        snippets = instance.snippets.all()
        serializer = SnippetSerializers(snippets, many=True, context={'request': request})
        return Response(serializer.data)



