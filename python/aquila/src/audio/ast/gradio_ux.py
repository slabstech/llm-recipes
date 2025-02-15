import gradio as gr
from gradio_client import Client

def predict(audio):
    #client = Client("http://138.246.17.57:8000")
    client = Client("http://localhost:8000")
    result = client.predict(audio, api_name="/predict")
    return result

iface = gr.Interface(
    fn=predict,
    inputs=gr.Audio(type="filepath"),
    outputs="text",
    title="Audio Classification",
    description="Upload an audio file to get the predicted label."
)

iface.launch(share=True)
