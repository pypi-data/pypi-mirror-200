import django_filters
from django.forms import (
    CharField, FloatField, HiddenInput
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from netbox_storage.choices import DeviceTypeChoices

from netbox_storage.models import LinuxDevice
from utilities.forms import DynamicModelChoiceField, ChoiceField, add_blank_choice, StaticSelect


class LinuxDeviceForm(NetBoxModelForm):
    device = CharField(
        label="Device Name",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    type = ChoiceField(
        choices=add_blank_choice(DeviceTypeChoices),
        label="Device Type",
        help_text="The type of the device e.g. Disk, Partition, LVM",
        initial='',
        widget=StaticSelect()
    )
    size = FloatField(
        label="Size",
        help_text="The size of the device e.g. 200",
    )

    class Meta:
        model = LinuxDevice

        fields = (
            'content_type',
            'object_id',
            "device",
            "type",
            "size",
        )
        widgets = {
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
        }

"""
    def save(self, *args, **kwargs):
        object_pk = self.cleaned_data['parent_object'].pk

        self.instance.content_type_pk = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
        self.instance.object_id = object_pk

        linux_device = super().save(*args, **kwargs)

        return linux_device
"""


class LinuxDeviceFilterForm(NetBoxModelFilterSetForm):

    model = LinuxDevice

    device = CharField(
        label="Device",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )


class LinuxDeviceImportForm(NetBoxModelImportForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = LinuxDevice

        fields = (
            "device",
            "type",
        )


class LinuxDeviceBulkEditForm(NetBoxModelBulkEditForm):
    model = LinuxDevice

    device = CharField(
        required=False,
        label="Device",
    )
    type = CharField(
        required=False,
        label="Type",
    )

    fieldsets = (
        (
            None,
            ("device", "type"),
        ),
    )
