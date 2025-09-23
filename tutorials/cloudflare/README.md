Cloudflare tunnels

```bash
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update
sudo apt install cloudflared

cloudflared login



cloudflared tunnel --no-autoupdate run --token adadasdas
```
<!-- 
--

create ~/cloudflared/config.yml

cloudflared tunnel create dwani_laptop_2

cloudflared tunnel --loglevel debug run dwani_laptop_2


---
-->