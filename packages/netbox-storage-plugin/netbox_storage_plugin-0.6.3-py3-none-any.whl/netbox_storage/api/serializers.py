from rest_framework import serializers

from virtualization.api.serializers import NestedClusterSerializer, NestedVirtualMachineSerializer
from dcim.api.serializers import NestedDeviceSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from netbox.api.fields import SerializedPKRelatedField
from ..models import StoragePool, LUN, StorageSession, Datastore, VMDK


#
# Nested serializers
#

class NestedStoragePoolSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:storagepool-detail'
    )

    class Meta:
        model = StoragePool
        fields = ('id', 'url', 'display', 'name')


class NestedLUNSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:lun-detail'
    )

    class Meta:
        model = LUN
        fields = ('id', 'url', 'display', 'name')


class NestedDatastoreSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:datastore-detail'
    )

    class Meta:
        model = Datastore
        fields = ('id', 'url', 'display', 'name')


class NestedStorageSessionSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:storagesession-detail'
    )

    class Meta:
        model = StorageSession
        fields = ('id', 'url', 'display', 'name')


class NestedVMDKSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:vmdk-detail'
    )

    class Meta:
        model = VMDK
        fields = ('id', 'url', 'display', 'name')


#
# Regular serializers
#

class StoragePoolSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:storagepool-detail'
    )
    device = NestedDeviceSerializer()

    class Meta:
        model = StoragePool
        fields = (
            'id', 'url', 'display', 'name', 'size', 'device', 'description',
            'tags', 'custom_fields', 'created', 'last_updated',
        )


class LUNSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:lun-detail'
    )
    storage_pool = NestedStoragePoolSerializer()

    class Meta:
        model = LUN
        fields = (
            'id', 'url', 'display', 'name', 'size', 'storage_pool', 'wwn',
            'description', 'tags', 'custom_fields',
            'created', 'last_updated',
        )


class DatastoreSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:datastore-detail'
    )
    lun = SerializedPKRelatedField(
        queryset=LUN.objects.all(),
        serializer=NestedLUNSerializer,
        many=True
    )

    class Meta:
        model = Datastore
        fields = (
            'id', 'url', 'display', 'name', 'lun',
            'description', 'tags', 'custom_fields', 'created', 'last_updated',
        )


class StorageSessionSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:storagesession-detail'
    )
    cluster = NestedClusterSerializer()
    datastores = SerializedPKRelatedField(
        queryset=Datastore.objects.all(),
        serializer=NestedDatastoreSerializer,
        many=True
    )

    class Meta:
        model = StorageSession
        fields = (
            'id', 'url', 'display', 'name', 'cluster', 'datastores',
            'description', 'tags', 'custom_fields', 'created', 'last_updated',
        )


class VMDKSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_storage-api:vmdk-detail'
    )
    datastore = NestedDatastoreSerializer()
    vm = NestedVirtualMachineSerializer()

    class Meta:
        model = VMDK
        fields = (
            'id', 'url', 'display', 'vm', 'name', 'datastore',
            'size', 'tags', 'custom_fields', 'created', 'last_updated',
        )
