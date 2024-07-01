#from drone_control.record_video import start_360_capture
from drone_control.take_picture import image_capture
from drone_control.vision_query import explain_images_directory

from drone_control.model_setup import load_model

from battlefield.data_insights import generate_insights

def get_drone_video():
    print("getting drone video")
    file_name_for_video = "drone_360_video.avi"
    start_360_capture(file_name_for_video)
    return file_name_for_video

def get_drone_picture():
    print("getting dorne picture")
    file_name_for_image = "picture.png"
    image_capture(file_name_for_image)
    return file_name_for_image
    

   


def main():
    #drone_video = get_drone_video()
    #drone_picture = get_drone_picture()    
    
    ollama_url = "http://localhost:11434"
    model_name = "moondream:latest"
    load_model( ollama_url, model_name )
    model_name = "mistral:latest"
    load_model( ollama_url, model_name )

    directory = "/home/gaganyatri/code/hackathon/defense_hack/dataset/image_set_1"
    metadata_file_name=  explain_images_directory(directory)
        
    insight_file_name = generate_insights(metadata_file_name)

if __name__ == "__main__":
    main()