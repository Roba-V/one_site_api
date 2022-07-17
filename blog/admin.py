from django.contrib import admin
from .models import Category, Language, Tag


class LanguageAdmin(admin.ModelAdmin):
    """言語管理クラス"""

    # 一覧画面に表示するフィールド & リンクを貼り付ける一覧画面のフィールド
    list_display = list_display_links = ("name", "code")

    # 編集画面で表示するフィールド
    fieldsets = (
        (None, {"fields": ("name", "code", ("created_user", "updated_user"))}),
        (
            "オプション",
            {
                "classes": ("collapse",),
                "fields": ("sort", "alias"),
            },
        ),
    )


class TagAdmin(admin.ModelAdmin):
    """タグ管理クラス"""

    # 一覧画面に表示するフィールド & リンクを貼り付ける一覧画面のフィールド
    list_display = list_display_links = ("name", "language")

    # リストフィルター
    list_filter = ("language",)

    # 検索フィルター
    search_fields = ("name",)

    # 編集画面で表示するフィールド
    fieldsets = (
        (None, {"fields": ("name", ("created_user", "updated_user"), "language")}),
        (
            "オプション",
            {
                "classes": ("collapse",),
                "fields": ("sort", "alias"),
            },
        ),
        (
            "SEO",
            {
                "classes": ("collapse",),
                "fields": ("description", "keywords"),
            },
        ),
    )


class CategoryAdmin(admin.ModelAdmin):
    """カテゴリー管理クラス"""

    # 一覧画面に表示するフィールド & リンクを貼り付ける一覧画面のフィールド
    list_display = list_display_links = (
        "name",
        "category_type",
        "parent_category",
        "language",
    )

    # リストフィルター
    list_filter = ("category_type", "language")

    # 検索フィルター
    search_fields = ("name",)

    # 編集画面で表示するフィールド
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    ("category_type", "parent_category"),
                    ("created_user", "updated_user"),
                    "language",
                )
            },
        ),
        (
            "オプション",
            {
                "classes": ("collapse",),
                "fields": ("sort", "alias"),
            },
        ),
        (
            "SEO",
            {
                "classes": ("collapse",),
                "fields": ("description", "keywords"),
            },
        ),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Tag, TagAdmin)
