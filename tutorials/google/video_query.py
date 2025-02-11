
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# TODO(developer): Update and un-comment below line
# PROJECT_ID = "your-project-id"

vertexai.init(project=PROJECT_ID, location="us-central1")

model = GenerativeModel("gemini-1.5-flash-002")

prompt = """
Provide a description of the video.
The description should also contain anything important which people say in the video.
"""

video_file = Part.from_uri(
    uri="gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
    mime_type="video/mp4",
)

contents = [video_file, prompt]

response = model.generate_content(contents)
print(response.text)
# Example response:
# Here is a description of the video.
# ... Then, the scene changes to a woman named Saeko Shimada..
# She says, "Tokyo has many faces. The city at night is totally different
# from what you see during the day."
# ...
