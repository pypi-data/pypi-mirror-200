from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import TemplateConfigurationDrive


class TemplateConfigurationDriveFilter(NetBoxModelFilterSet):
    class Meta:
        model = TemplateConfigurationDrive
        fields = ["platform", "drive"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
