from netbox.api.routers import NetBoxRouter

from netbox_storage.api.views import (
    NetboxStorageRootView,
    DriveViewSet,
    FilesystemViewSet,
    PartitionViewSet,
    MountedVolumeViewSet,
    LinuxDeviceViewSet,
    LogicalVolumeViewSet,
    PhysicalVolumeViewSet,
    VolumeGroupViewSet,
    TemplateConfigurationDriveViewSet
)

router = NetBoxRouter()
router.APIRootView = NetboxStorageRootView

router.register("drive", DriveViewSet)
router.register("filesystem", FilesystemViewSet)
router.register("partition", PartitionViewSet)
router.register("mountedvolume", MountedVolumeViewSet)
router.register("linuxdevice", LinuxDeviceViewSet)
router.register("logicalvolume", LogicalVolumeViewSet)
router.register("physicalvolume", PhysicalVolumeViewSet)
router.register("volumegroup", VolumeGroupViewSet)
router.register("templateconfigurationdrive", TemplateConfigurationDriveViewSet)

urlpatterns = router.urls
