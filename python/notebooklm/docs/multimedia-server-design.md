Multimedia Server Design

- How to design multi-media storage for python/django tp provide audio services on deman
- Generate audio and store in cloud storage ?

- Use django-storage library for cdn?
  - Amazon s3, Azure Blob, Cloudflare cdn, Google Cloud Storage
  - Use nginx to serve static files

- Full system design
  - Network management
  - Database setup
  - Authentication
  - on-demand GPU server - For text to audio
  - How does Twitter/LinkedIn/Instagram/Youtube store User Generated Content


- Enable streaming with http range requests using nginx
- Convert adui files to HLS (Https Live streaming) format
- encode response/requests to base64 to reduce network bandwith