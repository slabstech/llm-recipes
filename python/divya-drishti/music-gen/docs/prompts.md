### Prompts for parser

- Prompt for Script parser into Structured scene

    ```
    You are given a script in a text format. Your task is to parse this script into a structured JSON format with the following requirements:

    Scenes: Break the script down into distinct scenes.
    Scene Title: Provide a descriptive title for each scene.
    Background Music: Describe the background music or ambient sounds for each scene.
    Sound Effects: List the specific sound effects that occur during each scene.
    Dialogue: List the dialogue lines with the speaker's name clearly indicated.
    Do not provide additional strings to json
    Ex. 
    {
        "scenes": [
        {
            "scene_title": "Forest Clearing",
            "background_music": "Soft, ambient forest sounds with wind whistling, leaves rustling, and birds chirping sporadically.",
            "sound_effects": [
            "A branch cracks in the distance.",
            "Echo of the cracking sound."
            ],
            "dialogue": [
            {
                "speaker": "Emma",
                "line": "So, Leo, what were you trying to show me here?"
            },
            {
                "speaker": "Leo",
                "line": "Patience, Emma. It's a bit... how should I say... next-level cool."
            },
            ]
        }
        ]
    }
    """

    ```

- Speaker Dialog Prompt for Parser

    ```
        The task is to analyze the given script and update the voice descriptions for each speaker based on the scene. 
        The initial voice descriptions provided a general overview of how each speaker sounds. 
        The updated script includes detailed voice descriptions for each line of dialogue, 
        incorporating the emotional nuances and specific tones relevant to each scene.
            speaker_1_description = """
                    Emma's voice is expressive and dramatic in delivery, speaking at a moderately fast pace with a very close recording that almost has no background noise.
                """
            speaker_2_description = """
                    Leo's voice is deep and resonant, with a calm and authoritative tone. He speaks at a steady pace, ensuring clarity and precision in his delivery. The recording is clear with minimal background noise, providing a professional and engaging listening experience.
                """
    ```

- Prompt parser for narrator description

    ```
    You are given a script for an audiobook that includes various scenes with background music, sound effects, and dialogue. Your task is to parse this script into a structured JSON format with the following requirements:

    Extract the scene titles: Include the scene_title for each scene.
    Describe the scenes: Provide a narrator_description for each scene that captures the atmosphere, sound effects, and actions, creating an immersive experience for the listener.
    Exclude speaker dialogues: Do not include any dialogue spoken by the characters; focus solely on the narrator's description of the scene.

    ```

- Prompt parser for narrator only description of audiobook
    ```
    Your task is to parse this script into a structured JSON format with the following requirements:

    Analyze the following scene for an audiobook, providing dialogs for the main narrator only. Ensure the analysis captures the atmosphere, sound effects, and dialogue to create an immersive experience for the listener.",
    
    ```

- Prompt for background music and sound effect with timestamps

    ```
    Task: Create an Immersive Audiobook Experience

    Objective: To create a detailed and immersive audiobook experience by structuring scenes with specific timestamps and durations for background music, sound effects, and dialogue. This will ensure a dynamic and engaging listening experience.

    Requirements:

    Scene Structure: Each scene should include:

    Scene Title
    Background Music with description, timestamp, and duration
    Sound Effects with description, timestamp, and duration
    Dialogue with speaker, line, timestamp, and duration
    Timestamps and Durations:

    Provide precise timestamps for when each background music, sound effect, and dialogue line starts.
    Include the duration for each background music, sound effect, and dialogue line.
    JSON Format: The final output should be in JSON format for easy integration into an audiobook production system.


    ```