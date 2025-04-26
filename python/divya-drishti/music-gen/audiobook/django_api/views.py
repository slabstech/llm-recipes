from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from your_app.models import Scene, BackgroundMusic, SoundEffect, Speaker, Dialogue
from your_app.serializers import SceneSerializer, BackgroundMusicSerializer, SoundEffectSerializer, SpeakerSerializer, DialogueSerializer

class ImportDataView(APIView):
    def post(self, request):
        data = request.data

        for scene_data in data['scenes']:
            scene_serializer = SceneSerializer(data={'scene_title': scene_data['scene_title']})
            if scene_serializer.is_valid():
                scene = scene_serializer.save()
            else:
                return Response(scene_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            background_music_serializer = BackgroundMusicSerializer(data={'scene': scene.id, 'description': scene_data['background_music']})
            if background_music_serializer.is_valid():
                background_music_serializer.save()
            else:
                return Response(background_music_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            for effect in scene_data['sound_effects']:
                sound_effect_serializer = SoundEffectSerializer(data={'scene': scene.id, 'description': effect})
                if sound_effect_serializer.is_valid():
                    sound_effect_serializer.save()
                else:
                    return Response(sound_effect_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            for dialogue_data in scene_data['dialogue']:
                speaker, _ = Speaker.objects.get_or_create(speaker_name=dialogue_data['speaker'])
                dialogue_serializer = DialogueSerializer(data={'scene': scene.id, 'speaker': speaker.id, 'line': dialogue_data['line']})
                if dialogue_serializer.is_valid():
                    dialogue_serializer.save()
                else:
                    return Response(dialogue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)