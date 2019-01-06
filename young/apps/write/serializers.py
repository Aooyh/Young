import re
from rest_framework import serializers

from apps.users.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'headline', 'content']
        read_only_fields = ['id']
        extra_kwargs = {
            'headline': {'max_length': 100, 'min_length': 5},
            'content': {'min_length': 1}
        }

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user.id
        content = validated_data['content']
        new_article = Article.objects.create(**validated_data)
        image = re.search('< img.*>?', content)
        if image:
            image = image.group()
            start = image.find('http')
            end = image.rfind('\"')
            focus_url = image[start:end]
            print(focus_url)
            new_article.focus_url = focus_url
            new_article.save()
        return new_article

    def update(self, instance, validated_data):
        instance.author = validated_data['author']
        instance.headline = validated_data['headline']
        instance.content = validated_data['content']
        instance.save()
        return instance
