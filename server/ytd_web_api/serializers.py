from rest_framework import serializers
from ytd_web_core.models import Downloadable

class DownloadableSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(source='name')
    valid_for = serializers.CharField(source='expiration_period')
    
    class Meta:
        model = Downloadable
        fields = ['file_name', 'valid_for']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["downloadable_link"] = self.context["request"].build_absolute_uri().split("/api")[0] + "/downloads/" + str(instance.id)

        return data
    