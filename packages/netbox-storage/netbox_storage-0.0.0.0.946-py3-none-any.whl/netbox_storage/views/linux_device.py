from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views.generic import ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView, BulkImportView, \
    BulkEditView, BulkDeleteView

from netbox_storage.filters import LinuxDeviceFilter
from netbox_storage.forms import (
    LinuxDeviceImportForm,
    LinuxDeviceFilterForm,
    LinuxDeviceForm,
    LinuxDeviceBulkEditForm
)

from netbox_storage.models import LinuxDevice
from netbox_storage.tables import LinuxDeviceTable


class LinuxDeviceListView(ObjectListView):
    queryset = LinuxDevice.objects.all()
    filterset = LinuxDeviceFilter
    filterset_form = LinuxDeviceFilterForm
    table = LinuxDeviceTable


class LinuxDeviceView(ObjectView):
    queryset = LinuxDevice.objects.all()


class LinuxDeviceEditView(ObjectEditView):
    queryset = LinuxDevice.objects.all()
    form = LinuxDeviceForm
    template_name = 'netbox_storage/linuxdevice_edit.html'

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            # Assign the object based on URL kwargs
            content_type = get_object_or_404(ContentType, pk=request.GET.get('content_type'))
            instance.object = get_object_or_404(content_type.model_class(), pk=request.GET.get('object_id'))
        return instance

    def get_extra_addanother_params(self, request):
        return {
            'content_type': request.GET.get('content_type'),
            'object_id': request.GET.get('object_id'),
        }


class LinuxDeviceDeleteView(ObjectDeleteView):
    queryset = LinuxDevice.objects.all()
    default_return_url = "plugins:netbox_storage:linuxdevice_list"


class LinuxDeviceBulkImportView(BulkImportView):
    queryset = LinuxDevice.objects.all()
    model_form = LinuxDeviceImportForm
    table = LinuxDeviceTable
    default_return_url = "plugins:netbox_storage:linuxdevice_list"


class LinuxDeviceBulkEditView(BulkEditView):
    queryset = LinuxDevice.objects.all()
    filterset = LinuxDeviceFilter
    table = LinuxDeviceTable
    form = LinuxDeviceBulkEditForm


class LinuxDeviceBulkDeleteView(BulkDeleteView):
    queryset = LinuxDevice.objects.all()
    table = LinuxDeviceTable
