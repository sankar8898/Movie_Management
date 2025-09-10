from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    title = serializers.CharField()
    poster = serializers.CharField()
    rating = serializers.FloatField()
    description = serializers.CharField()
