from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from netbox_storage.models import Drive, Filesystem, Partition, MountedVolume, LinuxDevice, LogicalVolume, VolumeGroup, \
    PhysicalVolume
from netbox_storage.views import (
    # Drive View
    DriveListView,
    DriveView,
    DriveAddView,
    DriveEditView,
    DriveDeleteView,
    DriveBulkImportView,
    DriveBulkEditView,
    DriveBulkDeleteView,
    DrivePartitionListView,
    # Filesystem Views
    FilesystemListView,
    FilesystemView,
    FilesystemEditView,
    FilesystemDeleteView,
    FilesystemBulkImportView,
    FilesystemBulkEditView,
    FilesystemBulkDeleteView,
    # Linux Device View
    LinuxDeviceListView,
    LinuxDeviceEditView,
    LinuxDeviceBulkImportView,
    LinuxDeviceBulkEditView,
    LinuxDeviceBulkDeleteView,
    LinuxDeviceView,
    LinuxDeviceDeleteView,
    # LogicalVolume Views
    LogicalVolumeDeleteView,
    LogicalVolumeEditView,
    LogicalVolumeView,
    LogicalVolumeListView,
    LogicalVolumeBulkImportView,
    LogicalVolumeBulkEditView,
    LogicalVolumeBulkDeleteView,
    # MountedVolume Views
    MountedVolumeListView,
    MountedVolumeEditView,
    MountedVolumeBulkImportView,
    MountedVolumeBulkEditView,
    MountedVolumeBulkDeleteView,
    MountedVolumeView,
    MountedVolumeDeleteView,
    # Partition Views
    PartitionListView,
    PartitionEditView,
    PartitionBulkImportView,
    PartitionBulkEditView,
    PartitionBulkDeleteView,
    PartitionView,
    PartitionDeleteView,
    # PhysicalVolume Views
    PhysicalVolumeDeleteView,
    PhysicalVolumeEditView,
    PhysicalVolumeView,
    PhysicalVolumeListView,
    PhysicalVolumeBulkImportView,
    PhysicalVolumeBulkEditView,
    PhysicalVolumeBulkDeleteView,
    # Simple Views
    LVMAddSimpleView,
    AddSimpleLinuxVolumeView,
    # Template Views
    TemplateLVMAddView,
    TemplatePartitionAddView,
    sys_topography_file,
    # VolumeGroup Views
    VolumeGroupDeleteView,
    VolumeGroupEditView,
    VolumeGroupView,
    VolumeGroupListView,
    VolumeGroupBulkImportView,
    VolumeGroupBulkEditView,
    VolumeGroupBulkDeleteView,
)

app_name = "netbox_storage"

urlpatterns = [
    #
    # Drive urls
    #
    path("drive/", DriveListView.as_view(), name="drive_list"),
    path("drive/add/", DriveAddView.as_view(), name="drive_add"),
    path("drive/import/", DriveBulkImportView.as_view(), name="drive_import"),
    path("drive/edit/", DriveBulkEditView.as_view(), name="drive_bulk_edit"),
    path("drive/delete/", DriveBulkDeleteView.as_view(), name="drive_bulk_delete"),
    path("drive/<int:pk>/", DriveView.as_view(), name="drive"),
    path("drive/<int:pk>/edit/", DriveEditView.as_view(), name="drive_edit"),
    path("drive/<int:pk>/delete/", DriveDeleteView.as_view(), name="drive_delete"),
    path(
        "drive/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="drive_changelog",
        kwargs={"model": Drive},
    ),
    path("drive/<int:pk>/partition/", DrivePartitionListView.as_view(), name="drive_partitions"),
    #
    # Filesystem urls
    #
    path("filesystem/", FilesystemListView.as_view(), name="filesystem_list"),
    path("filesystem/add/", FilesystemEditView.as_view(), name="filesystem_add"),
    path("filesystem/import/", FilesystemBulkImportView.as_view(), name="filesystem_import"),
    path("filesystem/edit/", FilesystemBulkEditView.as_view(), name="filesystem_bulk_edit"),
    path("filesystem/delete/", FilesystemBulkDeleteView.as_view(), name="filesystem_bulk_delete"),
    path("filesystem/<int:pk>/", FilesystemView.as_view(), name="filesystem"),
    path("filesystem/<int:pk>/edit/", FilesystemEditView.as_view(), name="filesystem_edit"),
    path("filesystem/<int:pk>/delete/", FilesystemDeleteView.as_view(), name="filesystem_delete"),
    path(
        "filesystem/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="filesystem_changelog",
        kwargs={"model": Filesystem},
    ),
    #
    # Partition urls
    #
    path("partition/", PartitionListView.as_view(), name="partition_list"),
    path("partition/add/", PartitionEditView.as_view(), name="partition_add"),
    path("partition/import/", PartitionBulkImportView.as_view(), name="partition_import"),
    path("partition/edit/", PartitionBulkEditView.as_view(), name="partition_bulk_edit"),
    path("partition/delete/", PartitionBulkDeleteView.as_view(), name="partition_bulk_delete"),
    path("partition/<int:pk>/", PartitionView.as_view(), name="partition"),
    path("partition/<int:pk>/edit/", PartitionEditView.as_view(), name="partition_edit"),
    path("partition/<int:pk>/delete/", PartitionDeleteView.as_view(), name="partition_delete"),
    path(
        "partition/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="partition_changelog",
        kwargs={"model": Partition},
    ),
    #
    # MountedVolume urls
    #
    path("mountedvolume/", MountedVolumeListView.as_view(), name="mountedvolume_list"),
    path("mountedvolume/add/", MountedVolumeEditView.as_view(), name="mountedvolume_add"),
    path("mountedvolume/import/", MountedVolumeBulkImportView.as_view(), name="mountedvolume_import"),
    path("mountedvolume/edit/", MountedVolumeBulkEditView.as_view(), name="mountedvolume_bulk_edit"),
    path("mountedvolume/delete/", MountedVolumeBulkDeleteView.as_view(), name="mountedvolume_bulk_delete"),
    path("mountedvolume/<int:pk>/", MountedVolumeView.as_view(), name="mountedvolume"),
    path("mountedvolume/<int:pk>/edit/", MountedVolumeEditView.as_view(), name="mountedvolume_edit"),
    path("mountedvolume/<int:pk>/delete/", MountedVolumeDeleteView.as_view(), name="mountedvolume_delete"),
    path(
        "mountedvolume/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="mountedvolume_changelog",
        kwargs={"model": MountedVolume},
    ),
    #
    # MountedVolume urls
    #
    path("linuxdevice/", LinuxDeviceListView.as_view(), name="linuxdevice_list"),
    path("linuxdevice/add/", LinuxDeviceEditView.as_view(), name="linuxdevice_add"),
    path("linuxdevice/import/", LinuxDeviceBulkImportView.as_view(), name="linuxdevice_import"),
    path("linuxdevice/edit/", LinuxDeviceBulkEditView.as_view(), name="linuxdevice_bulk_edit"),
    path("linuxdevice/delete/", LinuxDeviceBulkDeleteView.as_view(), name="linuxdevice_bulk_delete"),
    path("linuxdevice/<int:pk>/", LinuxDeviceView.as_view(), name="linuxdevice"),
    path("linuxdevice/<int:pk>/edit/", LinuxDeviceEditView.as_view(), name="linuxdevice_edit"),
    path("linuxdevice/<int:pk>/delete/", LinuxDeviceDeleteView.as_view(), name="linuxdevice_delete"),
    path(
        "linuxdevice/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="linuxdevice_changelog",
        kwargs={"model": LinuxDevice},
    ),
    #
    # Logical Volume urls
    #
    path("logicalvolume/", LogicalVolumeListView.as_view(), name="logicalvolume_list"),
    path("logicalvolume/add/", LogicalVolumeEditView.as_view(), name="logicalvolume_add"),
    path("logicalvolume/import/", LogicalVolumeBulkImportView.as_view(), name="logicalvolume_import"),
    path("logicalvolume/edit/", LogicalVolumeBulkEditView.as_view(), name="logicalvolume_bulk_edit"),
    path("logicalvolume/delete/", LogicalVolumeBulkDeleteView.as_view(), name="logicalvolume_bulk_delete"),
    path("logicalvolume/<int:pk>/", LogicalVolumeView.as_view(), name="logicalvolume"),
    path("logicalvolume/<int:pk>/edit/", LogicalVolumeEditView.as_view(), name="logicalvolume_edit"),
    path("logicalvolume/<int:pk>/delete/", LogicalVolumeDeleteView.as_view(), name="logicalvolume_delete"),
    path(
        "logicalvolume/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="logicalvolume_changelog",
        kwargs={"model": LogicalVolume},
    ),
    #
    # Volume Group urls
    #
    path("volumegroup/", VolumeGroupListView.as_view(), name="volumegroup_list"),
    path("volumegroup/add/", VolumeGroupEditView.as_view(), name="volumegroup_add"),
    path("volumegroup/import/", VolumeGroupBulkImportView.as_view(), name="volumegroup_import"),
    path("volumegroup/edit/", VolumeGroupBulkEditView.as_view(), name="volumegroup_bulk_edit"),
    path("volumegroup/delete/", VolumeGroupBulkDeleteView.as_view(), name="volumegroup_bulk_delete"),
    path("volumegroup/<int:pk>/", VolumeGroupView.as_view(), name="volumegroup"),
    path("volumegroup/<int:pk>/edit/", VolumeGroupEditView.as_view(), name="volumegroup_edit"),
    path("volumegroup/<int:pk>/delete/", VolumeGroupDeleteView.as_view(), name="volumegroup_delete"),
    path(
        "volumegroup/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="volumegroup_changelog",
        kwargs={"model": VolumeGroup},
    ),
    #
    # Physical Volume urls
    #
    path("physicalvolume/", PhysicalVolumeListView.as_view(), name="physicalvolume_list"),
    path("physicalvolume/add/", PhysicalVolumeEditView.as_view(), name="physicalvolume_add"),
    path("physicalvolume/import/", PhysicalVolumeBulkImportView.as_view(), name="physicalvolume_import"),
    path("physicalvolume/edit/", PhysicalVolumeBulkEditView.as_view(), name="physicalvolume_bulk_edit"),
    path("physicalvolume/delete/", PhysicalVolumeBulkDeleteView.as_view(), name="physicalvolume_bulk_delete"),
    path("physicalvolume/<int:pk>/", PhysicalVolumeView.as_view(), name="physicalvolume"),
    path("physicalvolume/<int:pk>/edit/", PhysicalVolumeEditView.as_view(), name="physicalvolume_edit"),
    path("physicalvolume/<int:pk>/delete/", PhysicalVolumeDeleteView.as_view(), name="physicalvolume_delete"),
    path(
        "physicalvolume/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="physicalvolume_changelog",
        kwargs={"model": PhysicalVolume},
    ),
    #
    # Simple Configuration
    #
    path('lvm-add/', LVMAddSimpleView.as_view(), name='lvm_add'),
    path('volume-add/', AddSimpleLinuxVolumeView.as_view(), name="volume_add"),
    #
    # Template Configuration
    #
    path('template-lvm-add/', TemplateLVMAddView.as_view(), name='template_lvm_add'),
    path('template-partition-add', TemplatePartitionAddView.as_view(), name='template_partition_add'),
    path('sync-template-to-vm/', sys_topography_file, name='sync-template-to-vm')
]
