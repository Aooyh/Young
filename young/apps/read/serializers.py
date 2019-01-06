from rest_framework import serializers

from apps.users.models import Article, User, Comment


class AuthorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'avatar_url']


class ArticleListSerializer(serializers.ModelSerializer):
    author = AuthorInfoSerializer()

    class Meta:
        model = Article
        fields = ['id', 'author', 'read_count', 'like_count',
                  'trans_count', 'headline', 'focus_url', 'create_time']
        read_only_fields = ['id']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = AuthorInfoSerializer()

    class Meta:
        model = Article
        exclude = ['is_delete', 'focus_url']
        read_only_fields = ['id']


class ParentCommentSerializer(serializers.ModelSerializer):
    author = AuthorInfoSerializer()

    class Meta:
        model = Comment
        fields = ['content', 'author']
        read_only_fields = ['id']


class SonCommentSerializer(serializers.ModelSerializer):
    author = AuthorInfoSerializer()

    class Meta:
        model = Comment
        exclude = ['is_delete', 'article']
        read_only_fields = ['id']


class ArticleCommentSerializer(serializers.ModelSerializer):
    author = AuthorInfoSerializer()
    parent = ParentCommentSerializer()
    son_comments = SonCommentSerializer(many=True)

    class Meta:
        model = Comment
        exclude = ['is_delete', 'article']

    def create(self, validated_data):
        validated_data.pop('son_comments')
        validated_data['author'] = self.context.get('request').user.id
        parent_id = self.context.get('comment_id')
        if parent_id:
            validated_data['parent'] = parent_id
        else:
            validated_data.pop('parent')
        new_comment = Comment.objects.create(validated_data)
        new_comment.article = self.context.get('pk')
        new_comment.save()
        return new_comment
