from django.dispatch import receiver
from django.db import models
from .models import ConversationModel,ConversationEncryptedModel
from .utils import detect_changes
from django.core.exceptions import ObjectDoesNotExist
import os,logging

logger = logging.getLogger('Field Change Logger')

@receiver(models.signals.pre_save, sender=ConversationModel)
def conversation_model_pre_save(sender, instance, **kwargs):
    try:
        detect_changes(sender,instance)
    except ObjectDoesNotExist as e:
        # this instance is being created and not updated.
        logger.info(f'{instance} has been created')
        return

@receiver(models.signals.pre_save, sender=ConversationEncryptedModel)
def conversation_encrypted_model_pre_save(sender,instance,**kwargs):
    try:
        detect_changes(sender,instance)
    except ObjectDoesNotExist as e:
        # this instance is being created and not updated.
        logger.info(f'{instance} has been created')
        return




