from rest_framework import serializers, viewsets

from blog.models import Article, Tag, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["url", "name", "created_at", "updated_at"]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ["url", "name", "created_at", "updated_at"]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = [
            "url",
            "id",
            "title",
            "overview",
            "content",
            "created_at",
            "updated_at",
            "category",
            "tags",
        ]


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializer
