from django.db import models
from django.contrib.auth.models import User


class MetaMixin(models.Model):
    class Meta:
        abstract = True

    alias = models.SlugField(null=True, blank=True)
    sort = models.IntegerField(default=0, verbose_name="ソート")
    created_at = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(
        User, related_name="created_%(class)s_set", on_delete=models.PROTECT
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_user = models.ForeignKey(
        User, related_name="updated_%(class)s_set", on_delete=models.PROTECT
    )


class SeoMixin(models.Model):
    class Meta:
        abstract = True

    description = models.CharField(max_length=120, null=True, blank=True)
    keywords = models.CharField(max_length=200, null=True, blank=True)


class Language(MetaMixin):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)


class LanguageMixin(models.Model):
    class Meta:
        abstract = True

    language = models.ForeignKey(Language, on_delete=models.PROTECT)


class Tag(MetaMixin, LanguageMixin, SeoMixin):
    name = models.CharField(max_length=100)


class Category(MetaMixin, LanguageMixin, SeoMixin):
    class CategoryType(models.IntegerChoices):
        CATEGORY = 1
        SERIES = 2

    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey("self", on_delete=models.PROTECT)
    category_type = models.IntegerField(choices=CategoryType.choices)

    def __str__(self):
        return self.name


class Article(MetaMixin, LanguageMixin, SeoMixin):
    title = models.CharField(max_length=250)
    published_at = models.DateTimeField(
        null=True, blank=True, verbose_name="公開日時", help_text="未来の時間を設定した場合に、予約公開になる。"
    )
    overview = models.CharField(max_length=500, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    content = models.TextField()
    file = models.FileField(upload_to="")
