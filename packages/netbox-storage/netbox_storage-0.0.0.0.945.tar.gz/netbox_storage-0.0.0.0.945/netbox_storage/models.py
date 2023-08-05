from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum, CharField, Manager
from django.urls import reverse

from netbox.models import NetBoxModel
from netbox_storage.choices import OSTypeChoices, DeviceTypeChoices


class Filesystem(NetBoxModel):
    filesystem = models.CharField(
        unique=True,
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ['filesystem', 'description']

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:filesystem', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.filesystem}'

    class Meta:
        ordering = ('filesystem', 'description')


class LinuxDevice(NetBoxModel):
    device = models.CharField(
        max_length=255,
    )
    type = models.CharField(
        max_length=255,
    )
    size = models.FloatField(
        verbose_name='Size (GB)'
    )
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveBigIntegerField()
    object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id'
    )

    clone_fields = ['device', 'type', 'size', 'content_type', 'object_id']

    class Meta:
        ordering = ['device', 'type', 'size', 'content_type', 'object_id']

    def __str__(self):
        return f'{self.device} ({self.type})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:linuxdevice', kwargs={'pk': self.pk})


class Drive(NetBoxModel):
    cluster = models.ForeignKey(
        to='virtualization.Cluster',
        on_delete=models.PROTECT,
        related_name='cluster_drive',
    )
    size = models.FloatField(
        verbose_name='Size (GB)'
    )
    identifier = models.CharField(
        max_length=255,
    )
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveBigIntegerField()
    object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ['cluster', 'size', 'identifier', 'content_type', 'object_id', 'description']

    prerequisite_models = (
        'virtualization.Cluster',
    )

    class Meta:
        ordering = ['content_type', 'object_id', 'identifier', 'cluster', 'size']

    def __str__(self):
        return f'{self.identifier} ({self.size} GB {self.cluster})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:drive', kwargs={'pk': self.pk})

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/drive/'

    def partition_count(self):
        return Partition.objects.filter(drive=self).count()

    @property
    def free_space_on_drive(self):
        drive_type_id = ContentType.objects.get(app_label='netbox_storage', model='drive').pk
        linux_device_type_id = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
        # Get Linux Device of Drive e.g. /dev/sda
        linux_device_drive = LinuxDevice.objects.get(content_type_id=drive_type_id,
                                                     object_id=self.pk,
                                                     type=DeviceTypeChoices.CHOICE_DISK)

        if linux_device_drive is not None:
            linux_devices = LinuxDevice.objects.filter(type=DeviceTypeChoices.CHOICE_PARTITION,
                                                       content_type_id=linux_device_type_id,
                                                       object_id=linux_device_drive.pk)
            count_partition = linux_devices.count()
            if count_partition == 0:
                return self.size
            else:
                return self.size - linux_devices.aggregate(Sum('size'))['size__sum']
        else:
            if Partition.objects.filter(drive=self).count() == 0:
                return self.size
            else:
                return self.size - Partition.objects.filter(drive=self).aggregate(Sum('size'))['size__sum']

    def device_name(self):
        return f'/dev/sd{chr(ord("`") + int(self.identifier[-1]))}'

    def physicalvolumes_in_drive_count(self):
        return PhysicalVolume.objects.filter(drive=self).count()

    def delete(self, *args, **kwargs):
        if TemplateConfigurationDrive.objects.filter(drive=self).count() > 0:
            tcd = TemplateConfigurationDrive.objects.get(drive=self)
            print()
            tcd_list = TemplateConfigurationDrive.objects.filter(platform=tcd.platform).exclude(drive=self)
            super().delete(*args, **kwargs)
            for idx, tcd in enumerate(tcd_list):
                tcd.drive.identifier = f'Hard Drive {idx + 1}'
                print(f"New Identifier: {tcd.drive.identifier}")
                tcd.drive.save()
        elif StorageConfigurationDrive.objects.filter(drive=self).count() > 0:
            scd = StorageConfigurationDrive.objects.get(drive=self)
            print(f"StorageConfigurationDriveObject: {scd}")
            scd_list = StorageConfigurationDrive.objects.filter(virtual_machine=scd.virtual_machine).exclude(drive=self)
            print(f"StorageConfigurationDrive List: {scd_list}")
            super().delete(*args, **kwargs)
            for idx, scd in enumerate(scd_list):
                scd.drive.identifier = f'Hard Drive {idx + 1}'
                print(f"New Identifier: {scd.drive.identifier}")
                scd.drive.save()


    def left_free_space(self):
        current_partition_allocated_space = Partition.objects.filter(drive=self).aggregate(sum=Sum('size')).get(
            'sum') or 0
        return self.size - current_partition_allocated_space


class Partition(NetBoxModel):
    drive = models.ForeignKey(
        Drive,
        on_delete=models.CASCADE,
        related_name='drive_partition',
    )
    size = models.FloatField(
        verbose_name='Size (GB)'
    )
    fs_type = models.ForeignKey(
        Filesystem,
        on_delete=models.CASCADE,
        related_name='fs_partition',
        verbose_name='Filesystem',
    )
    letter = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ['drive', 'size', 'fs_type', 'letter', 'description']

    prerequisite_models = (
        'netbox_storage.Drive',
    )

    class Meta:
        ordering = ['drive', 'size', 'fs_type', 'letter', 'description']

    def __str__(self):
        return f'{self.letter}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:partition', kwargs={'pk': self.pk})

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/partition/'

    '''def clean(self, *args, **kwargs):
        total_allocated_space = Partition.objects.filter(drive=self.drive).aggregate(sum=Sum('size')).get('sum') or 0
        current_partition_size = Partition.objects.filter(drive=self.drive, id=self.pk) \
                                     .aggregate(sum=Sum('size')).get('sum') or 0
        if self.size is None:
            raise ValidationError(
                {
                    'size': f'The Value for Size must be greater than 0'
                }
            )
        diff_to_allocated_space = self.size - current_partition_size
        if diff_to_allocated_space > 0:
            if total_allocated_space == self.drive.size:
                raise ValidationError(
                    {
                        'size': f'The maximum Space of the hard drive was already allocated.'
                    }
                )
            if self.size > self.drive.size:
                raise ValidationError(
                    {
                        'size': f'The size of the Partition is bigger than the size of the Hard Drive.'
                    }
                )
            if total_allocated_space + self.size > self.drive.size:
                raise ValidationError(
                    {
                        'size': f'The size of the Partition is bigger than the size of the Hard Drive.'
                    }
                )
'''
    def get_affiliated_physical_volume(self):
        return PhysicalVolume.objects.filter(partition=self).first()


class VolumeGroup(NetBoxModel):
    vg_name = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        'vg_name',
        'description',
    ]

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:volumegroup', kwargs={'pk': self.pk})

    def __str__(self):
        return self.vg_name

    class Meta:
        ordering = ('vg_name', 'description')

    def physical_volume_count(self):
        return PhysicalVolume.objects.filter(vg=self).count()

    def logical_volume_count(self):
        return LogicalVolume.objects.filter(vg=self).count()

    def get_total_affiliated_size(self):
        total_sum = 0
        for PV in PhysicalVolume.objects.filter(vg=self):
            total_sum += PV.partition.size
        return total_sum


class PhysicalVolume(NetBoxModel):
    linux_device = models.ForeignKey(
        LinuxDevice,
        on_delete=models.CASCADE,
        related_name='linux_device_physicalvolume',
    )
    vg = models.ForeignKey(
        VolumeGroup,
        on_delete=models.CASCADE,
        related_name='volumegroup_physicalvolume',
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        'linux_device',
        'vg',
        'description',
    ]

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:physicalvolume', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.linux_device}'

    class Meta:
        ordering = ('linux_device', 'description')


class LogicalVolume(NetBoxModel):
    vg = models.ForeignKey(VolumeGroup, on_delete=models.CASCADE, related_name='volumegroup_logicalvolume')
    lv_name = models.CharField(
        max_length=255,
    )
    size = models.FloatField(
        verbose_name='Size (GB)'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        'vg',
        'lv_name',
        'size',
        'description',
    ]

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:logicalvolume', kwargs={'pk': self.pk})

    def __str__(self):
        return self.lv_name

    class Meta:
        ordering = ('lv_name', 'description')


class StorageConfigurationDrive(NetBoxModel):
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='virtual_machine_storage_configuration',
    )
    drive = models.ForeignKey(
        Drive,
        on_delete=models.CASCADE,
        related_name='drive_storage_configuration'
    )

    clone_fields = [
        'virtual_machine',
        'drive',
    ]

    class Meta:
        ordering = ['virtual_machine', 'drive']

    def __str__(self):
        return f'Storage Configuration of the VM {self.virtual_machine}'


class TemplateConfigurationDrive(NetBoxModel):
    platform = models.ForeignKey(
        to='dcim.platform',
        on_delete=models.CASCADE,
        related_name='platform_template_configuration',
    )
    drive = models.ForeignKey(
        Drive,
        on_delete=models.CASCADE,
        related_name='drive_template_configuration'
    )

    clone_fields = [
        'platform',
        'drive',
    ]

    class Meta:
        ordering = ['platform', 'drive']

    # def get_absolute_url(self):
    #     return reverse('plugins:netbox_storage:storageconfiguration', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Template Configuration of the Platform {self.platform} {self.drive}'


class MountedVolume(NetBoxModel):
    linux_device = models.ForeignKey(
        LinuxDevice,
        on_delete=models.CASCADE,
        related_name='linux_device_mounted_volume',
    )
    mount_point = models.CharField(
        max_length=255,
    )
    fs_type = models.ForeignKey(
        Filesystem,
        on_delete=models.CASCADE,
        related_name='fs_mounted_volume',
        verbose_name='Filesystem',
    )
    options = models.CharField(
        max_length=255,
        default='defaults',
        blank=True,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        'linux_device',
        'mount_point',
        'fs_type',
        'options',
        'description',
    ]

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:mountedvolume', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Filesystem Table Entry: mounted to {self.mount_point}'

    class Meta:
        ordering = ('linux_device', 'mount_point', 'fs_type', 'options', 'description')
