from django.contrib import admin
from django.db.models import Q
from .models import Tweet, Like


class ElonMuskFilter(admin.SimpleListFilter):
    title = 'Elon Musk'
    parameter_name = 'elon_musk'

    def lookups(self, request, model_admin):
        return (
            ('contains', 'Contains "Elon", "Musk", or "Elon Musk"'),
            ('not_contains', 'Does Not Contain "Elon", "Musk", or "Elon Musk"'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'contains':
            return queryset.filter(
                Q(payload__icontains='Elon') |
                Q(payload__icontains='Musk') |
                Q(payload__icontains='Elon Musk')
            )
        elif self.value() == 'not_contains':
            return queryset.exclude(
                Q(payload__icontains='Elon') |
                Q(payload__icontains='Musk') |
                Q(payload__icontains='Elon Musk')
            )
        return queryset


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('payload', 'user', 'created_at', 'updated_at')
    search_fields = ('payload', 'user__username')
    list_filter = (
        ElonMuskFilter,
        "created_at",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    search_fields = ("user__username",)
    list
