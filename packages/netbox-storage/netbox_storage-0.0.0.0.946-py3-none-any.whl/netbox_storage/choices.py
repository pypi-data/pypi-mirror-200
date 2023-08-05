from utilities.choices import ChoiceSet


class OSTypeChoices(ChoiceSet):
    key = 'StorageConfigurationDrive.type'

    CHOICE_LINUX = 'Linux'
    CHOICE_WINDOWS = 'Windows'

    CHOICES = [
        (CHOICE_LINUX, 'Linux', 'cyan'),
        (CHOICE_WINDOWS, 'Windows', 'yellow'),
    ]


class DeviceTypeChoices(ChoiceSet):
    key = 'LinuxDevice.type'

    CHOICE_DISK = 'Disk'
    CHOICE_PARTITION = 'Partition'
    CHOICE_LVM = 'LVM'

    CHOICES = [
        (CHOICE_DISK, 'Disk', 'cyan'),
        (CHOICE_PARTITION, 'Partition', 'yellow'),
        (CHOICE_LVM, 'LVM', 'red')
    ]
