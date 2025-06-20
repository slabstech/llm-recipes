cloudflare - subdoin setup

- Create a A record in DNS
  - provide dummy IP - 192.0.2.1
- Create a worker and update the code to
```js
export default {
  async fetch(request, env, ctx) {
    // Construct the new URL to forward the request to
    const url = new URL(request.url);
    url.hostname = "your-backend.example.com"; // Replace with your backend domain

    // Optionally, change the protocol or path here if needed
    // url.protocol = "https:";
    // url.pathname = "/new-path" + url.pathname;

    // Forward the request to the new URL
    const newRequest = new Request(url.toString(), request);
    return fetch(newRequest);
  }
}
```

Add - Route
    - test dwani ai and select the worker