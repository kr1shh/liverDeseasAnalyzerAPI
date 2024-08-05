# liver_prediction/serializers.py
from rest_framework import serializers

class LiverSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=[(0, 'Female'), (1, 'Male')])
    total_bilirubin = serializers.FloatField()
    direct_bilirubin = serializers.FloatField()
    alkaline_phosphotase = serializers.IntegerField()
    alamine_aminotransferase = serializers.IntegerField()
    total_proteins = serializers.FloatField()
    albumin = serializers.FloatField()
    albumin_and_globulin_ratio = serializers.FloatField()




class ChatbotResponseSerializer(serializers.Serializer):
    user_message = serializers.CharField()
    bot_response = serializers.CharField(read_only=True)

