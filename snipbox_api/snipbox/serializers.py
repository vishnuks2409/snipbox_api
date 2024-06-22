from rest_framework import serializers
from .models import Tags,Snippet
from django.contrib.auth.models import User
from rest_framework.reverse import reverse

"""Serializer class for Tags model"""
class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model=Tags
        fields = ['id','title']


"""Serializer class for Snippet model"""

class SnippetSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tags = TagSerializers(many=True)
    url = serializers.SerializerMethodField()
    class Meta:
        model=Snippet
        fields=['id','title', 'note', 'created', 'updated', 'user', 'tags','url']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('snippet-detail', args=[obj.id], request=request)
    #
    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        snippet = Snippet.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tags.objects.get_or_create(title=tag_data['title'])
            snippet.tags.add(tag)
        return snippet

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance.title = validated_data.get('title', instance.title)
        instance.note = validated_data.get('note', instance.note)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tags.objects.get_or_create(title=tag_data['title'])
            instance.tags.add(tag)
        return instance


"""Serializer class for User model"""
class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id','username','password']

    def create(self,validate_data):
        user=User.objects.create_user(username=validate_data['username'],
                                      password=validate_data['password'])
        user.save()
        return  user

