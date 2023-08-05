from . import models
from netbox.search import SearchIndex, register_search


@register_search
class DriveIndex(SearchIndex):
    model = models.Drive
    fields = (
        ('size', 100),
        ('identifier', 100),
        ('description', 100),
    )


@register_search
class PartitionIndex(SearchIndex):
    model = models.Partition
    fields = (
        ('letter', 100),
        ('size', 100),
        ('fs_type', 100),
        ('description', 100),
    )


@register_search
class VolumeGroupIndex(SearchIndex):
    model = models.VolumeGroup
    fields = (
        ('vg_name', 100),
        ('description', 100),
    )


@register_search
class PhysicalVolumeIndex(SearchIndex):
    model = models.PhysicalVolume
    fields = (
        ('description', 100),
    )


@register_search
class FilesystemIndex(SearchIndex):
    model = models.Filesystem
    fields = (
        ('filesystem', 100),
        ('description', 100),
    )


@register_search
class LogicalVolumeIndex(SearchIndex):
    model = models.LogicalVolume
    fields = (
        ('lv_name', 100),
        ('size', 100),
        ('description', 100),
    )


@register_search
class MountedVolumeIndex(SearchIndex):
    model = models.MountedVolume
    fields = (
        ('mount_point', 100),
        ('description', 100),
    )


@register_search
class LinuxDeviceIndex(SearchIndex):
    model = models.LinuxDevice
    fields = (
        ('device', 100),
        ('type', 100),
        ('size', 100),
        ('content_type', 100),
        ('object_id', 100),
    )