from rest_framework import serializers
from .models import MarkdownDocument, Tag
from .models import User
from django.contrib.auth import authenticate


from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class MarkdownDocumentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = MarkdownDocument
        fields = ['id', 'title', 'content', 'tags', 'created_at', 'updated_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        doc = MarkdownDocument.objects.create(owner=self.context['request'].user, **validated_data)
        for tag in tags_data:
            tag_obj, _ = Tag.objects.get_or_create(name=tag['name'])
            doc.tags.add(tag_obj)
        return doc

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        if tags_data:
            instance.tags.clear()
            for tag in tags_data:
                tag_obj, _ = Tag.objects.get_or_create(name=tag['name'])
                instance.tags.add(tag_obj)
        return instance
