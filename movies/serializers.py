from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    poster = serializers.CharField()
    rating = serializers.FloatField()
    description = serializers.CharField()
