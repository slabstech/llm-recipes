
ffmpeg commands

 - reducs fps to lower memory
    - ffmpeg -i input.mp4 -r 15 -c:v libx264 -c:a aac output.mp4

- Video  - webm to mp4 


    Prepare Your Files: Place your two WEBM files (let’s call them video1.webm and video2.webm) in the same folder.
    Create a Text File: Make a file called filelist.txt in the same folder and add these lines:

    file 'video1.webm'
    file 'video2.webm'

    Run the Command: Open a terminal or command prompt, navigate to the folder with your files, and run:

    ffmpeg -f concat -i filelist.txt -c:v libx264 -c:a aac output.mp4

    This concatenates the videos and converts them to MP4 with H.264 video and AAC audio, which is YouTube-friendly.
    Check the Output: You’ll get a file named output.mp4 ready for upload.

--------
- Video - webm to mp4  - With deduplication

     Place Your Files: Put your two WEBM files (e.g., video1.webm and video2.webm) in one folder.
    Remove Duplicates Within Each Video:
        Run this command for each file to filter out duplicate frames:

        ffmpeg -i video1.webm -vf mpdecimate -c:v libx264 -c:a aac video1_clean.mp4
        ffmpeg -i video2.webm -vf mpdecimate -c:v libx264 -c:a aac video2_clean.mp4

        The mpdecimate filter detects and drops frames that are nearly identical to the previous one, effectively removing duplicates. The output will be video1_clean.mp4 and video2_clean.mp4.
    Combine the Cleaned Videos:
        Create a filelist.txt file in the same folder with:

        file 'video1_clean.mp4'
        file 'video2_clean.mp4'

        Concatenate them into a single MP4:

        ffmpeg -f concat -i filelist.txt -c:v libx264 -c:a aac output.mp4

    Verify and Upload: Check output.mp4 to ensure it looks good, then upload it to YouTube.

