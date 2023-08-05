# General
## Build Project
To build the project go to log in the pypi web ui and get your token. Add your token to the local pypi config.
```
poetry config pypi-token.pypi pypi-XXXXX
```
After you made changes, change the version in the files pyproject.toml and netbox_storage/__init__.py

Now you can build and publish the project.
```
poetry publish --build
```

## Use Project
Link: https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

docker-compose build --no-cache && docker-compose build --no-cache && docker-compose up -d


## Directory structure

```
+- api - The API Classes, consitsts of Serializer, URL Mapper and Views
+- filters - Filters of the models, the implementation of the method search, for searching
+- forms - The ModelForm, ModelFilterForm, ModelImportForm, ModelBulkEditForm, the forms which will be displayed
+- migrations - DB Django Migration steps
+- tables - The ModelTable, which has the configuration on how the table looks like
+- templates
  +- netbox_storage - The detail view of each model
    +- drive - The template content of drive, with base and partition model
    +- inc - The template content box in the Virtual Machine Model
    +- partition - The template content of partition, with base and physicalvolume model
    +- physicalvolume - The template content of physicalvolume with base and linuxvolume model
    +- volumegroup - The template content of volumegroup with base, logicalvolume and physicalvolume
+- views - PhysicalvolumeListView, PhysicalvolumeView, PhysicalvolumeEditView, PhysicalvolumeDeleteView, 
           PhysicalvolumeBulkImportView, PhysicalvolumeBulkEditView, PhysicalvolumeBulkDeleteView
```
### Models
#### ERM

![The ERM of the Project](documents/erm.jpg?raw=true "ERM Diagram")

#### Drive
The drive has 4 parameter:

| Name           |           Example Value           |
|:---------------|:---------------------------------:|
| Virtualmachine | test-vm (Link zu virtual machine) |
| Identifier     |           Festplatte 1            |
| Cluster        |   STOR2000000 (Link zu cluster)   |
| Size           |               50GB                |
| System         |                No                 |

#### Filesystem
The filesystem has 1 parameter:

| Name | Example Value |
|:-----|:-------------:|
| fs   |     EXT4      |



git add . && git commit -m "0.0.0.0.272" && git push

