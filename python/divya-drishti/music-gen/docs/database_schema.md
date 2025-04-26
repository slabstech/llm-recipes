Database Schema

Tables
Scenes
BackgroundMusic
SoundEffects
Dialogues
Speakers

1. Scenes

This table stores information about each scene.

CREATE TABLE Scenes (
    scene_id INT PRIMARY KEY AUTO_INCREMENT,
    scene_title VARCHAR(255) NOT NULL
);

2. BackgroundMusic

This table stores background music information for each scene.

CREATE TABLE BackgroundMusic (
    music_id INT PRIMARY KEY AUTO_INCREMENT,
    scene_id INT,
    description TEXT,
    FOREIGN KEY (scene_id) REFERENCES Scenes(scene_id)
);

3. SoundEffects
This table stores sound effects information for each scene.

CREATE TABLE SoundEffects (
    effect_id INT PRIMARY KEY AUTO_INCREMENT,
    scene_id INT,
    description TEXT,
    FOREIGN KEY (scene_id) REFERENCES Scenes(scene_id)
);

4. Dialogues
This table stores dialogue information for each scene.

CREATE TABLE Dialogues (
    dialogue_id INT PRIMARY KEY AUTO_INCREMENT,
    scene_id INT,
    speaker_id INT,
    line TEXT,
    FOREIGN KEY (scene_id) REFERENCES Scenes(scene_id),
    FOREIGN KEY (speaker_id) REFERENCES Speakers(speaker_id)
);

5. Speakers
This table stores information about the speakers.

CREATE TABLE Speakers (
    speaker_id INT PRIMARY KEY AUTO_INCREMENT,
    speaker_name VARCHAR(255) NOT NULL
);


Explanation

Scenes: This table stores the basic information about each scene, such as the scene title.
BackgroundMusic: This table stores the background music description for each scene.
SoundEffects: This table stores the sound effects descriptions for each scene.
Dialogues: This table stores the dialogue lines for each scene, including the speaker and the line of dialogue.
Speakers: This table stores the names of the speakers.


Relationships
Scenes and BackgroundMusic: One scene can have one background music description.
Scenes and SoundEffects: One scene can have multiple sound effects.
Scenes and Dialogues: One scene can have multiple dialogues.
Speakers and Dialogues: One speaker can have multiple dialogues.
This schema ensures that all the information from the JSON is properly stored and related in a relational database.


-- 
Standalone script for entry

python import_data.py

-- 
rest api call

curl -X POST http://127.0.0.1:8000/import-data/ -H "Content-Type: application/json" -d @structured_scene.json
