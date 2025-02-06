from rest_framework import serializers
from your_app.models import Scene, BackgroundMusic, SoundEffect, Speaker, Dialogue

class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = '__all__'

class BackgroundMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundMusic
        fields = '__all__'

class SoundEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoundEffect
        fields = '__all__'

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'

class DialogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialogue
        fields = '__all__'