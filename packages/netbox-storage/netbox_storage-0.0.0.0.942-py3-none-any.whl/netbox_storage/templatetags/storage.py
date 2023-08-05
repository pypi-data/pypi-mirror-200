from django import template
from django.contrib.contenttypes.models import ContentType

from netbox_storage.models import LinuxDevice

register = template.Library()


@register.simple_tag
def get_partition_amount(drive):
    drive_type_id = ContentType.objects.get(app_label='netbox_storage', model='drive').pk
    linux_device_type_id = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
    # Get Linux Device of Drive e.g. /dev/sda
    linux_device_drive = LinuxDevice.objects.get(content_type_id=drive_type_id, object_id=drive.pk,
                                                 type='Disk')
    # Wenn es keine Partition hat zu lonely_drives hinzufügen
    if LinuxDevice.objects.filter(content_type_id=linux_device_type_id, object_id=linux_device_drive.pk,
                                  type='Partition').count() == 0:
        return f"0"
    else:
        count = LinuxDevice.objects.filter(content_type_id=linux_device_type_id, object_id=linux_device_drive.pk,
                                           type='Partition').count()
        return f"{count}"


@register.simple_tag
def get_partitions(drive):
    drive_type_id = ContentType.objects.get(app_label='netbox_storage', model='drive').pk
    linux_device_type_id = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
    linux_device_drive = LinuxDevice.objects.get(content_type_id=drive_type_id, object_id=drive.pk,
                                                 type='Disk')
    if LinuxDevice.objects.filter(content_type_id=linux_device_type_id, object_id=linux_device_drive.pk,
                                  type='Partition').count() == 0:
        return []
    else:
        return list(LinuxDevice.objects.filter(content_type_id=linux_device_type_id,
                                               object_id=linux_device_drive.pk, type='Partition'))
