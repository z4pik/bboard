from rest_framework import serializers

from main.models import Bb, Comment


class BbSerializer(serializers.ModelSerializer):
    """Получаем список всех объявлений"""
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at')


class BbDetailSerializer(serializers.ModelSerializer):
    """Подробная информация о конкретном объявление"""
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at', 'contacts', 'image')


class CommentSerializer(serializers.ModelSerializer):
    """Комментарии"""
    class Meta:
        model = Comment
        fields = ('bb', 'author', 'content', 'created_at')
