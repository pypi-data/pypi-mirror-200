from django.contrib.contenttypes.models import ContentType

from extras.plugins import PluginTemplateExtension
from netbox_storage.models import LogicalVolume, StorageConfigurationDrive, \
    TemplateConfigurationDrive, Drive, Partition, LinuxDevice, MountedVolume


class VMTemplateContent(PluginTemplateExtension):
    model = "virtualization.virtualmachine"

    def left_page(self):
        obj = self.context.get("object")

        drives_id = StorageConfigurationDrive.objects.values('drive').filter(virtual_machine=obj)
        partition_dict = {}
        for drive_id in drives_id:
            print(f"Drive ID: {drive_id['drive']}")
            drive = Drive.objects.get(pk=drive_id['drive'])

            if Partition.objects.filter(drive=drive).count() == 0:
                partition_dict[drive] = None
            else:
                partition_dict[drive] = list(Partition.objects.filter(drive=drive))

        platform = obj.platform
        if platform is not None:
            if platform.name.lower().__contains__('windows'):
                return self.render(
                    "netbox_storage/inc/vm_windows_box.html",
                    extra_context={
                        "partition_dict": partition_dict,
                    },
                )
            elif platform.name.lower().__contains__('linux'):
                return self.render(
                    "netbox_storage/inc/linuxvolume_box.html"
                )
        else:
            return self.render(
                "netbox_storage/inc/unknown_os_box.html"
            )


class PlatformTemplateContent(PluginTemplateExtension):
    model = "dcim.platform"

    def right_page(self):
        obj = self.context.get("object")
        parent_object_type = ContentType.objects.get(app_label='dcim', model='platform').pk

        if obj.name.lower().__contains__('windows'):
            drives = Drive.objects.filter(content_type=parent_object_type, object_id=obj.pk)
            partition_dict = {}
            for drive in drives:
                if Partition.objects.filter(drive=drive).count() == 0:
                    partition_dict[drive] = None
                else:
                    partition_dict[drive] = list(Partition.objects.filter(drive=drive))
            return self.render(
                "netbox_storage/inc/template_windows_drive_box.html",
                extra_context={
                    "partition_dict": partition_dict,
                },
            )
        else:
            drives_id = Drive.objects.filter(content_type=parent_object_type, object_id=obj.pk)
            partition_dict = {}
            for drive in drives_id:
                drive_type_id = ContentType.objects.get(app_label='netbox_storage', model='drive').pk
                linux_device_type_id = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
                # Get Linux Device of Drive e.g. /dev/sda
                linux_device_drive = LinuxDevice.objects.get(content_type_id=drive_type_id,
                                                             object_id=drive.pk,
                                                             type='Disk')

                if LinuxDevice.objects.filter(content_type_id=linux_device_type_id,
                                              object_id=linux_device_drive.pk,
                                              type='Partition').count() == 0:
                    partition_dict[drive] = None
                else:
                    partition_dict[drive] = list(LinuxDevice.objects.filter(content_type_id=linux_device_type_id,
                                                                            object_id=linux_device_drive.pk,
                                                                            type='Partition'))
            return self.render(
                "netbox_storage/inc/template_drive_box.html",
                extra_context={
                    "partition_dict": partition_dict
                }
            )

    def left_page(self):
        obj = self.context.get("object")
        mounted_volumes = MountedVolume.objects.all()
        if obj.name.lower().__contains__('windows'):
            return self.render(
                "netbox_storage/inc/nothing.html",
            )
        else:
            return self.render(
                "netbox_storage/inc/template_volume_box.html",
                extra_context={
                    "mounted_volumes": mounted_volumes
                }
            )


template_extensions = [VMTemplateContent, PlatformTemplateContent]
