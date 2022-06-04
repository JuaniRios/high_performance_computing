from rest_framework import serializers
from .models import Job, Result


# Custom serializers using Django Rest Framework
class JobSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField()
    status_verbose = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Job
        fields = "__all__"


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"
