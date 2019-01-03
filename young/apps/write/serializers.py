from apps.users.models import Article

from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'author', 'headline', 'content']
        read_only_fields = ['id']
        extra_kwargs = {
            'headline': {'max_length': 100, 'min_length': 5},
            'content': {'min_length': 1}
        }

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.author = validated_data['author']
        instance.headline = validated_data['headline']
        instance.content = validated_data['content']
        instance.save()
        return instance
