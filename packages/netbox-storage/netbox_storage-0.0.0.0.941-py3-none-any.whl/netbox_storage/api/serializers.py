from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from dcim.api.nested_serializers import NestedPlatformSerializer
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox.constants import NESTED_SERIALIZER_PREFIX
from netbox_storage.api.nested_serializers import NestedFilesystemSerializer, NestedDriveSerializer, \
    NestedMountedVolumeSerializer, NestedLinuxDeviceSerializer, NestedVolumeGroupSerializer
from netbox_storage.models import Drive, Filesystem, Partition, MountedVolume, StorageConfigurationDrive, \
    LinuxDevice, TemplateConfigurationDrive, PhysicalVolume, VolumeGroup, LogicalVolume
from utilities.api import get_serializer_for_model
from virtualization.api.nested_serializers import NestedClusterSerializer, NestedVirtualMachineSerializer


class FilesystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filesystem
        fields = (
            "id",
            "filesystem",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class DriveSerializer(NetBoxModelSerializer):
    cluster = NestedClusterSerializer(required=False, allow_null=True)
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_storage-api:drive-detail")
    content_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = Drive
        fields = (
            "id",
            "url",
            "display",
            "size",
            "cluster",
            "identifier",
            'content_type',
            'object_id',
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class PartitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_storage-api:partition-detail')
    drive = NestedDriveSerializer(required=False, allow_null=True)
    fs_type = NestedFilesystemSerializer(required=False, allow_null=True)

    class Meta:
        model = Partition
        fields = (
            "id",
            "url",
            "drive",
            "size",
            "fs_type",
            "letter",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class MountedVolumeSerializer(serializers.ModelSerializer):
    fs_type = NestedFilesystemSerializer(required=False, allow_null=True)

    class Meta:
        model = MountedVolume
        fields = (
            "id",
            "mount_point",
            "fs_type",
            "options",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class LinuxDeviceSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )
    object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LinuxDevice
        fields = (
            "id",
            "device",
            "type",
            "size",
            'content_type', 'object_id', 'object',
            "created",
            "last_updated",
            "custom_fields",
        )

    @swagger_serializer_method(serializer_or_field=serializers.JSONField)
    def get_object(self, instance):
        # serializer = get_serializer_for_model(instance.content_type.model_class(), prefix=NESTED_SERIALIZER_PREFIX)
        serializer = get_serializer_for_model(instance.content_type.model_class())
        context = {'request': self.context['request']}
        return serializer(instance.object, context=context).data


class PhysicalVolumeSerializer(serializers.ModelSerializer):
    linux_device = NestedLinuxDeviceSerializer(required=False, allow_null=True)
    vg = NestedVolumeGroupSerializer(required=False, allow_null=True)

    class Meta:
        model = PhysicalVolume
        fields = (
            "id",
            "linux_device",
            "vg",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class VolumeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = VolumeGroup
        fields = (
            "id",
            "vg_name",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class LogicalVolumeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:logicalvolume-detail"
    )
    vg = NestedVolumeGroupSerializer(required=False, allow_null=True)

    class Meta:
        model = LogicalVolume
        fields = (
            "id",
            'url',
            "vg",
            "lv_name",
            "size",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class StorageConfigurationDriveSerializer(serializers.ModelSerializer):
    drive = NestedDriveSerializer(required=False, allow_null=True)
    virtual_machine = NestedVirtualMachineSerializer(required=False, allow_null=True)

    class Meta:
        model = StorageConfigurationDrive
        fields = (
            "id",
            "drive",
            "virtual_machine",
            "created",
            "last_updated",
            "custom_fields",
        )


class TemplateConfigurationDriveSerializer(serializers.ModelSerializer):
    drive = NestedDriveSerializer(required=False, allow_null=True)
    platform = NestedPlatformSerializer(required=False, allow_null=True)

    class Meta:
        model = TemplateConfigurationDrive
        fields = (
            "id",
            "platform",
            "drive",
            "created",
            "last_updated",
            "custom_fields",
        )
