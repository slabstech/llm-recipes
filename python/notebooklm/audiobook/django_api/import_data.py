import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from your_app.models import Scene, BackgroundMusic, SoundEffect, Speaker, Dialogue

with open('path/to/your/structured_scene.json', 'r') as file:
    data = json.load(file)

for scene_data in data['scenes']:
    scene = Scene.objects.create(scene_title=scene_data['scene_title'])

    BackgroundMusic.objects.create(
        scene=scene,
        description=scene_data['background_music']
    )

    for effect in scene_data['sound_effects']:
        SoundEffect.objects.create(
            scene=scene,
            description=effect
        )

    for dialogue_data in scene_data['dialogue']:
        speaker, _ = Speaker.objects.get_or_create(speaker_name=dialogue_data['speaker'])
        Dialogue.objects.create(
            scene=scene,
            speaker=speaker,
            line=dialogue_data['line']
        )

print('Data imported successfully')