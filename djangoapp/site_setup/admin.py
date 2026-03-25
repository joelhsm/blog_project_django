from django.contrib import admin
from .models import MenuLink, SiteSetup

# Register your models here.

# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = ('text', 'url_or_path', 'new_tab')
#     list_display_links = ('text', 'url_or_path',)
#     list_filter = ('new_tab',)
#     search_fields = ('text', 'url_or_path')
#     ordering = ('text',)
#     list_editable = ('new_tab',)


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',

    inlines = [MenuLinkInline]

    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()


