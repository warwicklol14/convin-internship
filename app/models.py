from django.db import models
from .utils import compute_hash_of_file
import uuid,hashlib,os

def user_directory_path(instance,filename:str):
    return f'convos/{filename}'

class ConversationModel(models.Model):
    convo_text = models.CharField(verbose_name="Conversation Text",max_length=100)
    convo_audio = models.FileField(verbose_name="Conversation Audio File",upload_to=user_directory_path)

    def __str__(self):
        return str(self.convo_text)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

class ConversationEncryptedModel(models.Model):
    convo_audio = models.FileField(verbose_name="Conversation Audio File",upload_to=user_directory_path)
    convo_encrypted = models.CharField(verbose_name="Conversation Hash",max_length=100,blank=True,editable=False)

    def save(self,*args,**kwargs):
        with self.convo_audio.open('rb') as f:
            self.convo_encrypted = compute_hash_of_file(f)
            super(ConversationEncryptedModel,self).save(*args,**kwargs)

    class Meta:
        verbose_name = "Encrypted Conversation"
        verbose_name_plural = "Encrypted Conversations"


    

