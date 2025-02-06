from django.db import models

class Scene(models.Model):
    scene_title = models.CharField(max_length=255)

class BackgroundMusic(models.Model):
    scene = models.OneToOneField(Scene, on_delete=models.CASCADE)
    description = models.TextField()

class SoundEffect(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    description = models.TextField()

class Speaker(models.Model):
    speaker_name = models.CharField(max_length=255)

class Dialogue(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    line = models.TextField()