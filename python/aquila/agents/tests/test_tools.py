"""
This module contains unit tests for the tool functions in the military decision agent system.
"""

import unittest
from unittest.mock import patch, MagicMock
from tools import analyze_video, transcribe_audio, analyze_text

class TestTools(unittest.TestCase):

    @patch('cv2.VideoCapture')
    @patch('tensorflow.keras.applications.resnet50.ResNet50')
    def test_analyze_video(self, mock_resnet, mock_video_capture):
        mock_video_capture.return_value.get.return_value = 100
        mock_video_capture.return_value.read.return_value = (True, MagicMock())
        mock_resnet.return_value.predict.return_value = MagicMock()

        result = analyze_video("dummy_video.mp4")
        self.assertIn("Video analysis complete", result)

    @patch('langchain.document_loaders.AssemblyAIAudioTranscriptLoader')
    def test_transcribe_audio(self, mock_loader):
        mock_loader.return_value.load.return_value = [MagicMock(page_content="Transcribed text")]
        result = transcribe_audio("dummy_audio.wav")
        self.assertEqual(result, "Transcribed text")

    @patch('config.llm')
    def test_analyze_text(self, mock_llm):
        mock_llm.return_value = "Analysis summary"
        result = analyze_text("Test military report")
        self.assertEqual(result, "Analysis summary")

if __name__ == '__main__':
    unittest.main()
