To set up asdasdapi.dwani.ai in Cloudflare so that it proxies (forwards) requests to another URL—while keeping the original URL in the browser (not a redirect)—the recommended approach is to use Cloudflare Workers as a reverse proxy. Page Rules and Bulk Redirects only perform HTTP redirects, which change the URL in the browser, and are not suitable for transparent proxying[6][8].

## Steps to Proxy asdasdapi.dwani.ai to Another URL Using Cloudflare Workers

**1. Set up your DNS**
- In your Cloudflare dashboard, add a DNS record for aasdasdpi.dwani.ai pointing to any IP (e.g., 192.0.2.1) and ensure it is proxied (orange cloud).

**2. Create a Cloudflare Worker**
- Use the Cloudflare dashboard or the Wrangler CLI to create a new Worker[2][7].
- The Worker will intercept requests to asdasdapi.dwani.ai and forward them to your target backend URL, returning the response.

**Example Worker Script (JavaScript/TypeScript):**
```javascript
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
- Deploy this Worker.

**3. Route Traffic to the Worker**
- In the Cloudflare dashboard, set a route for your Worker, e.g.:
  - Route: `asdasdapi.dwani.ai/*`
  - Worker: (select your Worker)

**4. Test**
- Requests to asdasdapi.dwani.ai will now be transparently proxied to your backend URL, and the original URL will remain in the user's browser.

## Why Not Use Page Rules or Redirects?
- Page Rules and Bulk Redirects only perform HTTP redirects (301/302), which change the browser's URL and do not proxy the request[6][8].
- Workers allow you to intercept, modify, and forward requests while keeping the URL unchanged for the client[6][7].

## Additional Notes
- If you need to add authentication, logging, or modify headers, you can enhance the Worker script accordingly.
- This approach is scalable and works for any API or backend, including AI services.

**References:**  
[6]: Cloudflare Community - How to proxy requests to a particular path to another domain  
[2]: Cloudflare Workers AI Docs - Getting Started  
[7]: YouTube - Build a Simple API with Cloudflare Workers

If you need a step-by-step guide for deploying with Wrangler CLI or want to see advanced Worker examples, let me know!

[1] https://developers.cloudflare.com/ai-gateway/get-started/
[2] https://developers.cloudflare.com/workers-ai/get-started/workers-wrangler/
[3] https://developers.cloudflare.com/workers-ai/get-started/rest-api/
[4] https://www.youtube.com/watch?v=a3FuUbyEET0
[5] https://www.pulumi.com/ai/answers/ru7gJCXizN27eUZ1ZthkdV/configuring-cloudflare-access-for-ai-api-gateways
[6] https://community.cloudflare.com/t/how-to-proxy-requests-to-a-particular-path-to-another-domain/593388
[7] https://www.youtube.com/watch?v=dhVF7uTieAc
[8] https://www.pulumi.com/ai/answers/2DUHjEhHpi5W8MC4MqUV47/ai-api-routing-with-cloudflares-pagerules
[9] https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/