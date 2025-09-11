from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    poster = serializers.CharField()
    rating = serializers.CharField()
    description = serializers.CharField()
