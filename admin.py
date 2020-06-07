from django.contrib import admin

try:
    from modeltranslation.admin import TranslationAdmin

    ADMIN_MODEL = TranslationAdmin
except ImportError:
    TranslationAdmin = admin.ModelAdmin
    ADMIN_MODEL = TranslationAdmin

from postman.models import Information, Recipient, Email
from postman.forms import RecipientForm, EmailForm


# Register your models here.


class GroupAdmin(admin.ModelAdmin):
    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "One %s was" % self.__class__.__name__
        else:
            message_bit = "%s %ss where were" % (queryset.count(), self.__class__.__name__)

        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "Delete selected entries"


class TranslationGroupAdmin(ADMIN_MODEL):
    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "One %s was" % self.__class__.__name__
        else:
            message_bit = "%s %ss where were" % (queryset.count(), self.__class__.__name__)

        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "Delete selected entries"


class RecipientAdmin(GroupAdmin):
    fields = ['email', 'is_default', ]
    list_display = ['email', 'is_default', ]
    list_filter = ['email', ]
    search_fields = ['email', ]
    form = RecipientForm


class EmailAdmin(GroupAdmin):
    fields = ['company', 'first_name', 'last_name', 'email', 'telephone', 'message', 'privacy_accepted',
              'received_on', 'sent']

    list_display = ['pk', 'email', 'first_name', 'last_name', 'privacy_accepted', 'received_on', 'sent']
    list_filter = ['first_name', 'last_name', 'email', 'sent']
    search_fields = ['first_name', 'last_name', 'email']
    form = EmailForm


class InformationAdmin(TranslationGroupAdmin):
    fields = ['name', 'title', 'text', ]
    list_display = ['name', 'title', 'text', ]
    list_filter = ['name', 'title', 'text', ]
    search_fields = ['name', 'title', 'text', ]


admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Email, EmailAdmin)
