from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, Comment
from django.contrib.auth.models import User

"""
https://www.django-rest-framework.org/api-guide/serializers/#customizing-listserializer-behavior
"""


class SnippetListSerializer(serializers.ListSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'code', 'language', 'linenos', 'style', 'title', 'owner_id')

    def update(self, instance, validated_data):
        # Maps for id->instance and id -> data item.
        snippet_mapping = {snippet.id: snippet for snippet in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for snippet_id, data in data_mapping.items():
            snippet = snippet_mapping.get(snippet_id, None)
            if snippet is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(snippet, data))

        # Perform deletions.
        for snippet_id, snippet in snippet_mapping.items():
            if snippet_id not in data_mapping:
                snippet.delete()

        return ret


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'supervisor', 'description'


class SnippetSimpleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()  # https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield

    def get_comments(self, obj):
        comments = obj.comments
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    class Meta:
        model = Snippet
        fields = '__all__'

class SnippetSerializer(serializers.Serializer):

    @classmethod
    def many_init(cls, *args, **kwargs):
        # Instantiate the child serializer.
        kwargs['child'] = cls()
        # Instantiate the parent list serializer.
        return SnippetListSerializer(*args, **kwargs)

    owner = serializers.ReadOnlyField(source='owner.username')  #
    #owner = UserSimpleSerializer()
    #owner_id = serializers.IntegerField(required=False)
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

    class Meta:
        list_serializer_class = SnippetListSerializer


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
