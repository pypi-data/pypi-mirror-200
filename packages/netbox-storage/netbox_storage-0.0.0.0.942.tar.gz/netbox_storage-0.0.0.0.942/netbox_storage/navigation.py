from extras.plugins import PluginMenuButton, PluginMenuItem
from extras.plugins import PluginMenu
from utilities.choices import ButtonColorChoices

drive_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:drive_list",
    link_text="Drives",
    permissions=["netbox_storage.drive_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:drive_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_drive"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:drive_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_drive"],
        ),
    ),
)

lv_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:logicalvolume_list",
    link_text="Logical Volumes",
    permissions=["netbox_storage.storage_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:logicalvolume_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_storage"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:logicalvolume_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_drive"],
        ),
    ),
)
vg_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:volumegroup_list",
    link_text="Volume Groups",
    permissions=["netbox_storage.storage_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:volumegroup_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_storage"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:volumegroup_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_drive"],
        ),
    ),
)
pv_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:physicalvolume_list",
    link_text="Physical Volume",
    permissions=["netbox_storage.storage_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:physicalvolume_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_storage"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:physicalvolume_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_disk"],
        ),
    ),
)

filesystem_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:filesystem_list",
    link_text="Filesystem",
    permissions=["netbox_storage.storage_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:filesystem_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_storage"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:filesystem_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_storage"],
        ),
    ),
)


partition_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:partition_list",
    link_text="Partition",
    permissions=["netbox_storage.disk_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:partition_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_disk"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:partition_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_disk"],
        ),
    ),
)

linux_device_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:linuxdevice_list",
    link_text="Linux Device",
    permissions=["netbox_storage.disk_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:linuxdevice_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_disk"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:linuxdevice_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_disk"],
        ),
    ),
)

mounted_volume_menu_item = PluginMenuItem(
    link="plugins:netbox_storage:mountedvolume_list",
    link_text="Mounted Volume",
    permissions=["netbox_storage.disk_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_storage:mountedvolume_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_storage.add_disk"],
        ),
        PluginMenuButton(
            "plugins:netbox_storage:mountedvolume_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_storage.add_disk"],
        ),
    ),
)

menu = PluginMenu(
    label="NetBox Storage",
    groups=(
        (
            "General Configuration",
            (
                filesystem_menu_item,
            ),
        ),
        (
            "Linux & LVM Configuration",
            (
                mounted_volume_menu_item,
                lv_menu_item,
                vg_menu_item,
                pv_menu_item,
                linux_device_menu_item
            ),
        ),
        (
            "Windows Volume Configuration",
            (
                partition_menu_item,
            ),
        ),
        (
            "Storage Configuration",
            (
                drive_menu_item,
            ),
        ),

    ),
    icon_class="mdi mdi-disc",
)
