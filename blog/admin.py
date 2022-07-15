from django.contrib import admin
from .models import Language


class LanguageAdmin(admin.ModelAdmin):
    """言語管理クラス"""

    # 一覧画面に表示するフィールド
    list_display = ("name", "code")

    # リンクを貼り付ける一覧画面のフィールド
    list_display_links = ("name", "code")

    # 編集画面で表示するフィールド
    fieldsets = (
        (None, {"fields": ("name", "code", ("created_user", "updated_user"))}),
        (
            "オプション",
            {
                "classes": ("collapse",),
                "fields": ("alias", "sort"),
            },
        ),
    )


admin.site.register(Language, LanguageAdmin)
