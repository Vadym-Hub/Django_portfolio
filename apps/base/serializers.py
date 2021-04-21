from rest_framework import serializers


class WithoutParentListSerializer(serializers.ListSerializer):
    """
    A type of `ListSerializer` that may be used
    for writing custom serializer, who haven't parent.
    """
    def to_representation(self, data):
        """
        Return data, filtered by parent=none.
        """
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """
    A type of `Serializer` that may be used
    for writing custom serializer,
    that recursive hem self when he have children.
    """
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
