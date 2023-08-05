from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_storage.api.serializers import (
    DriveSerializer,
    FilesystemSerializer, PartitionSerializer, MountedVolumeSerializer, LinuxDeviceSerializer, LogicalVolumeSerializer,
    PhysicalVolumeSerializer, VolumeGroupSerializer, TemplateConfigurationDriveSerializer
)
from netbox_storage.filters import DriveFilter, FilesystemFilter, \
    PartitionFilter, MountedVolumeFilter, LinuxDeviceFilter, PhysicalVolumeFilter, VolumeGroupFilter, \
    LogicalVolumeFilter, TemplateConfigurationDriveFilter
from netbox_storage.models import Drive, Filesystem, Partition, MountedVolume, LinuxDevice, LogicalVolume, \
    PhysicalVolume, VolumeGroup, TemplateConfigurationDrive


class NetboxStorageRootView(APIRootView):
    """
    NetboxDNS API root view
    """

    def get_view_name(self):
        return "NetboxStorage"


class DriveViewSet(NetBoxModelViewSet):
    queryset = Drive.objects.all()
    serializer_class = DriveSerializer
    filterset_class = DriveFilter

    @action(detail=True, methods=["get"])
    def drive(self, request, pk=None):
        drives = Drive.objects.filter(drive__id=pk)
        serializer = DriveSerializer(drives, many=True, context={"request": request})
        return Response(serializer.data)


class FilesystemViewSet(NetBoxModelViewSet):
    queryset = Filesystem.objects.all()
    serializer_class = FilesystemSerializer
    filterset_class = FilesystemFilter

    @action(detail=True, methods=["get"])
    def filesystem(self, request, pk=None):
        filesystem = Filesystem.objects.filter(filesystem__id=pk)
        serializer = FilesystemSerializer(filesystem, many=True, context={"request": request})
        return Response(serializer.data)


class PartitionViewSet(NetBoxModelViewSet):
    queryset = Partition.objects.all()
    serializer_class = PartitionSerializer
    filterset_class = PartitionFilter

    @action(detail=True, methods=["get"])
    def partition(self, request, pk=None):
        partition = Partition.objects.filter(partition__id=pk)
        serializer = PartitionSerializer(partition, many=True, context={"request": request})
        return Response(serializer.data)


class MountedVolumeViewSet(NetBoxModelViewSet):
    queryset = MountedVolume.objects.all()
    serializer_class = MountedVolumeSerializer
    filterset_class = MountedVolumeFilter

    @action(detail=True, methods=["get"])
    def mountedvolume(self, request, pk=None):
        mountedvolume = MountedVolume.objects.filter(mountedvolume__id=pk)
        serializer = MountedVolumeSerializer(mountedvolume, many=True, context={"request": request})
        return Response(serializer.data)


class LinuxDeviceViewSet(NetBoxModelViewSet):
    queryset = LinuxDevice.objects.all()
    serializer_class = LinuxDeviceSerializer
    filterset_class = LinuxDeviceFilter

    @action(detail=True, methods=["get"])
    def linuxdevice(self, request, pk=None):
        linuxdevice = LinuxDevice.objects.filter(linuxdevice__id=pk)
        serializer = LinuxDeviceSerializer(linuxdevice, many=True, context={"request": request})
        return Response(serializer.data)


class LogicalVolumeViewSet(NetBoxModelViewSet):
    queryset = LogicalVolume.objects.all()
    serializer_class = LogicalVolumeSerializer
    filterset_class = LogicalVolumeFilter

    @action(detail=True, methods=["get"])
    def logicalvolume(self, request, pk=None):
        logicalvolume = LogicalVolume.objects.filter(logicalvolume__id=pk)
        serializer = LogicalVolumeSerializer(logicalvolume, many=True, context={"request": request})
        return Response(serializer.data)


class PhysicalVolumeViewSet(NetBoxModelViewSet):
    queryset = PhysicalVolume.objects.all()
    serializer_class = PhysicalVolumeSerializer
    filterset_class = PhysicalVolumeFilter

    @action(detail=True, methods=["get"])
    def physicalvolume(self, request, pk=None):
        physicalvolume = PhysicalVolume.objects.filter(physicalvolume__id=pk)
        serializer = PhysicalVolumeSerializer(physicalvolume, many=True, context={"request": request})
        return Response(serializer.data)


class VolumeGroupViewSet(NetBoxModelViewSet):
    queryset = VolumeGroup.objects.all()
    serializer_class = VolumeGroupSerializer
    filterset_class = VolumeGroupFilter

    @action(detail=True, methods=["get"])
    def volumegroup(self, request, pk=None):
        volumegroup = VolumeGroup.objects.filter(volumegroup__id=pk)
        serializer = VolumeGroupSerializer(volumegroup, many=True, context={"request": request})
        return Response(serializer.data)


class TemplateConfigurationDriveViewSet(NetBoxModelViewSet):
    queryset = TemplateConfigurationDrive.objects.all()
    serializer_class = TemplateConfigurationDriveSerializer
    filterset_class = TemplateConfigurationDriveFilter

    @action(detail=True, methods=["get"])
    def templateconfigurationdrive(self, request, pk=None):
        templateconfigurationdrive = TemplateConfigurationDrive.objects.filter(volumegroup__id=pk)
        serializer = TemplateConfigurationDriveSerializer(templateconfigurationdrive, many=True, context={"request": request})
        return Response(serializer.data)
