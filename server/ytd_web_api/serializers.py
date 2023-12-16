from rest_framework import serializers
from ytd_web_core.models import Downloadable
from configparser import ConfigParser

config = ConfigParser()
config.read(".env")
_server_ip = config["server"]["ip"]

class DownloadableSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(source='name')
    valid_for = serializers.CharField(source='expiration_period')
    downloadable_link = serializers.CharField(source='name')
    
    class Meta:
        model = Downloadable
        fields = ['file_name', 'valid_for', 'downloadable_link']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["downloadable_link"] = _server_ip + "/downloads/" + str(instance.id)

        return data
    
class QualitiesSerializer(serializers.Serializer):
    audio_qualities = serializers.ListField()
    video_qualities = serializers.ListField()
    
class SingleSearchResultSerializer(serializers.Serializer):
    video_id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.CharField()
    channel_name = serializers.CharField()
    channel_thumbnail_url = serializers.CharField()

class SearchResultsSerializer(serializers.Serializer):
    results=serializers.ListField(child=SingleSearchResultSerializer())
