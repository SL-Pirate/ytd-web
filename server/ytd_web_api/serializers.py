from rest_framework import serializers
from ytd_web_core.models import Downloadable

class DownloadableSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(source='name')
    valid_for = serializers.CharField(source='expiration_period')
    downloadable_link = serializers.CharField(source='name')
    
    class Meta:
        model = Downloadable
        fields = ['file_name', 'valid_for', 'downloadable_link']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["downloadable_link"] = self.context["request"].build_absolute_uri().split("/api")[0] + "/downloads/" + str(instance.id)

        return data
    
class QualitiesSerializer(serializers.Serializer):
    audio_qualities = serializers.ListField()
    video_qualities = serializers.ListField()
    
class SingleSearchResultSerializer(serializers.Serializer):
    video_id = serializers.CharField()
    title = serializers.CharField()
    thumbnail_url = serializers.CharField()
    channel_name = serializers.CharField()

class SearchResultsSerializer(serializers.Serializer):
    results=serializers.ListField(child=SingleSearchResultSerializer())