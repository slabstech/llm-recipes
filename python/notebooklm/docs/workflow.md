## Detailed Workflow:

Workflow - Optimised for Production

1. User upload PDF/Doc to Main Page
2. Entry is made in DB for Async Main Actions Run
3. Entry is made into celery for creating async calls to 
  - Script parser - LLM : Large Context
  - Script is split into Sessions and session is split into background music, narrator and speakers
  - Calls are executed Session by session for Human feedback.
  - Async calls for audio gen for backgound music with script-id, session-id, background-music-id
  - Async call on TTS service is made for each session for narraor, different speakers with session-id, speaker-turn-id
  - Based on GPU availability, Async call's can be run in linear or parallel ( Later optimisation problem) 
4. Script Parser
  - Using structured outputs, splits the scripts into different session based on template. Scene, Background Score, Conversation
  - Background score is split into distinct sounds and approximate duration for audio generation
  - Conversation is analysed and Voice-description for each session is updated based on Inputs. 
    Ex 
    - Emma (whispering)
        - Leo… What have you done?
    - Leo (excited)
        - I think… we just discovered something big.
  - Narrator voice is chosen and given a distinct personality based on user choice.

---
---
LLM Generated


1. **User Uploads PDF/Doc:**
   - User uploads the document via a user-friendly interface.
   - The system validates the document format and integrity.
   - Confirmation message is displayed to the user.

2. **Database Entry:**
   - An entry is made in the database for the new document.
   - Log the entry and handle any potential errors.

3. **Async Tasks with Celery:**
   - Tasks are created in Celery with clear dependencies.
   - Script parsing and session splitting tasks are initiated.
   - Human feedback tasks are scheduled.
   - Audio generation tasks are queued, considering GPU availability.
   - Retry mechanism is implemented for failed tasks.

4. **Script Parser:**
   - The script is parsed using structured outputs.
   - Sessions are split based on the template, with flexibility for different formats.
   - Background scores are accurately split into distinct sounds.
   - Conversations are analyzed for context and emotions.
   - Voice descriptions are generated using advanced NLP techniques.
   - Narrator voice is chosen based on user preference, with options for preview.

5. **Quality Assurance:**
   - The generated audiobook is reviewed for quality and consistency.
   - User notifications are sent at each stage of the process.

6. **User Feedback:**
   - Collect feedback from users to improve the process.
   - Implement changes based on user feedback.


# Workflow Improvements for Creating Audiobook

## 1. User Upload PDF/Doc to Main Page
- **User Interface:** Provide a more intuitive and user-friendly interface for uploading documents. Include progress bars and confirmation messages.
- **Validation:** Implement a validation step to ensure the uploaded file is in the correct format and is not corrupted.

## 2. Entry is made in DB for Async Main Actions Run
- **Error Handling:** Implement robust error handling to manage cases where the database entry fails.
- **Logging:** Add detailed logging for each step to facilitate debugging and monitoring.

## 3. Entry is made into Celery for creating async calls
- **Task Dependencies:** Clearly define task dependencies to ensure that tasks are executed in the correct order.
- **Retry Mechanism:** Implement a retry mechanism for failed tasks with exponential backoff.
- **Monitoring:** Use a monitoring tool like Flower to monitor Celery tasks in real-time.

### Subtasks:
- **Script Parser - LLM:** Ensure the parser can handle various script formats and structures.
- **Session Splitting:** Improve the algorithm for splitting scripts into sessions and further into background music, narrator, and speakers.
- **Human Feedback:** Incorporate a feedback loop where human reviewers can provide feedback on the generated sessions.
- **Audio Generation:** Optimize audio generation tasks to reduce latency.
- **TTS Service:** Ensure the TTS service supports multiple languages and accents.
- **GPU Availability:** Implement a dynamic scheduling mechanism to optimize GPU usage based on availability.

## 4. Script Parser
- **Template Flexibility:** Make the template-based splitting more flexible to handle different script formats.
- **Background Score:** Improve the accuracy of splitting background scores into distinct sounds and durations.
- **Conversation Analysis:** Enhance the analysis of conversations to better understand the context and emotions.
- **Voice-Description:** Use advanced NLP techniques to generate more accurate voice descriptions.
- **Narrator Voice:** Provide more options for narrator voices and personalities, and allow users to preview different voices before making a choice.

## Additional Improvements:
- **User Notifications:** Implement a notification system to keep users informed about the progress of their audiobook creation.
- **Quality Assurance:** Introduce a quality assurance step where the generated audiobook is reviewed for consistency and quality before final delivery.
- **User Feedback:** Collect user feedback on the final audiobook to continuously improve the process.
- **Scalability:** Ensure the system is scalable to handle a large number of concurrent tasks and users.
