from django.contrib import admin

from .models import ConversationModel,ConversationEncryptedModel

admin.site.register(ConversationModel)
admin.site.register(ConversationEncryptedModel)
