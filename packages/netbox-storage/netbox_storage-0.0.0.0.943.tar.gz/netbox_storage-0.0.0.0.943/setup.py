# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_storage',
 'netbox_storage.api',
 'netbox_storage.filters',
 'netbox_storage.forms',
 'netbox_storage.migrations',
 'netbox_storage.tables',
 'netbox_storage.templatetags',
 'netbox_storage.views']

package_data = \
{'': ['*'],
 'netbox_storage': ['templates/netbox_storage/*',
                    'templates/netbox_storage/drive/*',
                    'templates/netbox_storage/inc/*',
                    'templates/netbox_storage/partition/*']}

setup_kwargs = {
    'name': 'netbox-storage',
    'version': '0.0.0.0.943',
    'description': 'Netbox Storage Plugin',
    'long_description': '# General\n## Build Project\nTo build the project go to log in the pypi web ui and get your token. Add your token to the local pypi config.\n```\npoetry config pypi-token.pypi pypi-XXXXX\n```\nAfter you made changes, change the version in the files pyproject.toml and netbox_storage/__init__.py\n\nNow you can build and publish the project.\n```\npoetry publish --build\n```\n\n## Use Project\nLink: https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins\n\ndocker-compose build --no-cache && docker-compose build --no-cache && docker-compose up -d\n\n\n## Directory structure\n\n```\n+- api - The API Classes, consitsts of Serializer, URL Mapper and Views\n+- filters - Filters of the models, the implementation of the method search, for searching\n+- forms - The ModelForm, ModelFilterForm, ModelImportForm, ModelBulkEditForm, the forms which will be displayed\n+- migrations - DB Django Migration steps\n+- tables - The ModelTable, which has the configuration on how the table looks like\n+- templates\n  +- netbox_storage - The detail view of each model\n    +- drive - The template content of drive, with base and partition model\n    +- inc - The template content box in the Virtual Machine Model\n    +- partition - The template content of partition, with base and physicalvolume model\n    +- physicalvolume - The template content of physicalvolume with base and linuxvolume model\n    +- volumegroup - The template content of volumegroup with base, logicalvolume and physicalvolume\n+- views - PhysicalvolumeListView, PhysicalvolumeView, PhysicalvolumeEditView, PhysicalvolumeDeleteView, \n           PhysicalvolumeBulkImportView, PhysicalvolumeBulkEditView, PhysicalvolumeBulkDeleteView\n```\n### Models\n#### ERM\n\n![The ERM of the Project](documents/erm.jpg?raw=true "ERM Diagram")\n\n#### Drive\nThe drive has 4 parameter:\n\n| Name           |           Example Value           |\n|:---------------|:---------------------------------:|\n| Virtualmachine | test-vm (Link zu virtual machine) |\n| Identifier     |           Festplatte 1            |\n| Cluster        |   STOR2000000 (Link zu cluster)   |\n| Size           |               50GB                |\n| System         |                No                 |\n\n#### Filesystem\nThe filesystem has 1 parameter:\n\n| Name | Example Value |\n|:-----|:-------------:|\n| fs   |     EXT4      |\n\n\n\ngit add . && git commit -m "0.0.0.0.272" && git push\n\n',
    'author': 'Tim Rhomberg',
    'author_email': 'timrhomberg@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
