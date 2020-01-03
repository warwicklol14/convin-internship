import os,logging,hashlib

logger = logging.getLogger('Field Change Logger')

def compute_hash_of_file(f):
    hash = hashlib.sha1()
    if f.multiple_chunks():
        for chunk in f.chunks():
            hash.update(chunk)
    else:    
        hash.update(f.read())
    return hash.hexdigest()

def get_previous_instance(sender,instance):
    table_pk = instance._meta.pk.name
    table_pk_value = instance.__dict__[table_pk]
    query_kwargs = dict()
    query_kwargs[table_pk] = table_pk_value
    return sender.objects.get(**query_kwargs)

def get_instance_attribute(instance,field):
    return instance.__getattribute__(field.attname)

def is_field_changed(prev_instance,instance,field) -> bool:
    if(field.get_internal_type() == 'FileField'):
        return compute_hash_of_file(prev_instance.convo_audio) != compute_hash_of_file(instance.convo_audio)
    if(get_instance_attribute(prev_instance,field) != get_instance_attribute(instance,field)):
        return True
    else:
        return False

def detect_changes(sender,instance):
    prev_instance = get_previous_instance(sender,instance)
    fields = prev_instance._meta.get_fields()
    for field in fields:
        if(is_field_changed(prev_instance,instance,field)):
            change_string = (f'{field.name} of id {instance.id} '
                f'has been changed from {get_instance_attribute(prev_instance,field)} '
                f'to {get_instance_attribute(instance,field)}')
            logger.info(change_string)