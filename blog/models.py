from django.db import models
from django.contrib.auth.models import User


class MetaMixin(models.Model):
    """メタ情報ミックスイン抽象モデル"""

    class Meta:
        abstract = True

    # 別名
    alias = models.SlugField(
        null=True, blank=True, verbose_name="別名", help_text="URL でアクセスする時に使用する識別子"
    )

    # ソート
    sort = models.IntegerField(default=0, verbose_name="ソート", help_text="値の若い順で表示される。")

    # 作成者
    created_user = models.ForeignKey(
        User,
        related_name="created_%(class)s_set",
        on_delete=models.PROTECT,
        verbose_name="作成者",
    )

    # 最終更新者
    updated_user = models.ForeignKey(
        User,
        related_name="updated_%(class)s_set",
        on_delete=models.PROTECT,
        verbose_name="最終更新者",
    )

    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)

    # 最終更新日時
    updated_at = models.DateTimeField(auto_now=True)


class SeoMixin(models.Model):
    """SEOミックスイン抽象モデル"""

    class Meta:
        abstract = True

    # メタディスクリプション
    description = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name="メタディスクリプション",
        help_text="最大120文字まで入力できる。",
    )

    # メタキーワード
    keywords = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="メタキーワード",
        help_text="5つを目安として入力する。",
    )


class Language(MetaMixin):
    """言語モデル"""

    class Meta:
        verbose_name = verbose_name_plural = "言語"
        ordering = ("sort",)

    # 言語名称
    name = models.CharField(max_length=50, verbose_name="言語名称")

    # 言語コード
    code = models.CharField(max_length=20, verbose_name="言語コード")

    def __str__(self) -> str:
        return self.name


class LanguageMixin(models.Model):
    """言語ミックスイン抽象モデル"""

    class Meta:
        abstract = True

    # 言語（外部キー）
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name="言語")


class Tag(MetaMixin, LanguageMixin, SeoMixin):
    """タグモデル"""

    class Meta:
        verbose_name = verbose_name_plural = "タグ"
        ordering = ("sort",)

    # タグ名称
    name = models.CharField(max_length=100, verbose_name="タグ名称")

    def __str__(self) -> str:
        return self.name


class Category(MetaMixin, LanguageMixin, SeoMixin):
    """カテゴリーモデル"""

    class CategoryType(models.IntegerChoices):
        CATEGORY = 1, "カテゴリー"
        SERIES = 2, "シリーズ"

    class Meta:
        verbose_name = verbose_name_plural = "カテゴリー"
        ordering = ("sort",)

    # カテゴリー名称
    name = models.CharField(max_length=100, verbose_name="カテゴリー名称")

    # 親カテゴリー
    parent_category = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, verbose_name="親カテゴリー"
    )

    # カテゴリータイプ
    category_type = models.IntegerField(
        choices=CategoryType.choices, verbose_name="カテゴリータイプ"
    )

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
