import vertexai

from vertexai.generative_models import GenerativeModel, Part

# TODO(developer): Update and un-comment below line
# PROJECT_ID = "your-project-id"
vertexai.init(project=PROJECT_ID, location="us-central1")

model = GenerativeModel("gemini-1.5-flash-002")

response = model.generate_content(
    [
        Part.from_uri(
            "gs://cloud-samples-data/generative-ai/image/scones.jpg",
            mime_type="image/jpeg",
        ),
        "What is shown in this image?",
    ]
)

print(response.text)
# That's a lovely overhead shot of a rustic-style breakfast or brunch spread.
# Here's what's in the image:
# * **Blueberry scones:** Several freshly baked blueberry scones are arranged on parchment paper.
# They look crumbly and delicious.
# ...
