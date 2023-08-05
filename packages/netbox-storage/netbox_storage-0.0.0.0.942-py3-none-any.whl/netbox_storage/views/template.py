from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404

from netbox.views import generic
from netbox_storage.forms import LVMTemplateForm, LinuxDeviceForm

from netbox_storage.forms.template import PartitionTemplateForm
from netbox_storage.models import TemplateConfigurationDrive, Partition, LogicalVolume, LinuxDevice, Drive, \
    StorageConfigurationDrive

from django.http import HttpResponseRedirect

from virtualization.models import VirtualMachine


class TemplateLVMAddView(generic.ObjectEditView):
    queryset = LogicalVolume.objects.all()
    form = LVMTemplateForm
    template_name = 'netbox_storage/lvm_create.html'


class TemplatePartitionAddView(generic.ObjectEditView):
    queryset = LinuxDevice.objects.all()
    form = PartitionTemplateForm


class SyncTemplateToVMView(generic.ObjectEditView):
    queryset = StorageConfigurationDrive.objects.all()

    def get_extra_context(self, request, instance):
        print(f"Request: {request}")
        print(f"Self: {self}")
        print(f"Instance: {instance}")
        drives_id = TemplateConfigurationDrive.objects.values('drive').filter(platform=instance.platform)
        partition_dict = {}
        for drive_id in drives_id:
            drive = Drive.objects.get(pk=drive_id['drive'])

            if Partition.objects.filter(drive=drive).count() == 0:
                partition_dict[drive] = None
            else:
                partition_dict[drive] = list(Partition.objects.filter(drive=drive))

        for k, v in partition_dict.items():
            instance_drive = k
            instance_drive.pk = None
            instance_drive.save()
            StorageConfigurationDrive.objects.create(virtual_machine=instance, drive=instance_drive)

            for partition in v:
                instance_partition = partition
                instance_partition.pk = None
                instance_partition.drive = instance_drive
                instance_partition.save()
            print(k, v)
        return {}


def sys_topography_file(request):
    print(request)
    q = request.GET.get('q', '')
    vm = VirtualMachine.objects.get(pk=q)

    drives_id = TemplateConfigurationDrive.objects.values('drive').filter(platform=vm.platform)
    partition_dict = {}
    for drive_id in drives_id:
        drive = Drive.objects.get(pk=drive_id['drive'])

        if Partition.objects.filter(drive=drive).count() == 0:
            partition_dict[drive] = None
        else:
            partition_dict[drive] = list(Partition.objects.filter(drive=drive))

    for k, v in partition_dict.items():
        instance_drive = k
        instance_drive.pk = None

        number_of_hard_drives = StorageConfigurationDrive.objects.filter(
            virtual_machine=vm).count() or 0
        instance_drive.identifier = f'Hard Drive {number_of_hard_drives + 1}'

        instance_drive.save()
        StorageConfigurationDrive.objects.create(virtual_machine=vm, drive=instance_drive)

        for partition in v:
            instance_partition = partition
            instance_partition.pk = None
            instance_partition.drive = instance_drive
            instance_partition.save()
        print(k, v)

    return HttpResponseRedirect(vm.get_absolute_url())
