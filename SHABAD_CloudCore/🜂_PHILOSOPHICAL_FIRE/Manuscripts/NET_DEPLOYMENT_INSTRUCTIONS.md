# GhostCORE Money Pipeline – Safe Remote Access

**⚠️ Nikoli ne izpostavi storitev brez avtentikacije in TLS.** Uporabi vsaj VPN/SSH tunel ali reverse proxy z geslom in certifikatom.

## 1) Lokalen zagon
- Backend: `cd /home/saba/Desktop/ProPublica/AGENT_SYSTEMS/GHOSTCORE_AGENCY && ./start_money_server.sh` (port 5002).
- Dashboard: `cd /home/saba/Desktop/ShobadOS && python3 -m http.server 8082 --bind 0.0.0.0`.
- Lokalni dostop: `http://localhost:8082/Dashboard/integration_dashboard.html`.

## 2) Najbolj varno: VPN ali SSH tunel
- **VPN (WireGuard/OpenVPN):** izpostavi 5002 in 8082 samo znotraj VPN mreže.
- **SSH tunel (reverse)** z oddaljenega strežnika:
  - Backend: `ssh -R 5002:localhost:5002 user@remote.host`
  - Frontend: `ssh -R 8082:localhost:8082 user@remote.host`
- Dostop nato prek `http://remote.host:8082/...` (samo za prijavljene uporabnike na strežniku/VPN).

## 3) Reverse proxy z nginx (https + basic auth)
1. Na strežniku namesti nginx + certbot (Let’s Encrypt). 
2. Ustvari basic-auth uporabnika: `sudo htpasswd -c /etc/nginx/.htpasswd admin`.
3. Primer strežnika (prilagodi domene/porte):

```nginx
server {
  listen 80;
  server_name your.domain;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl;
  server_name your.domain;

  ssl_certificate /etc/letsencrypt/live/your.domain/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/your.domain/privkey.pem;

  auth_basic "Protected";
  auth_basic_user_file /etc/nginx/.htpasswd;

  location /api/ {
    proxy_pass http://127.0.0.1:5002/;
    proxy_set_header Host $host;
  }

  location / {
    proxy_pass http://127.0.0.1:8082/;
    proxy_set_header Host $host;
  }
}
```

4. Zaženi backend (5002) in dashboard (8082) na strežniku; v brskalniku odpri `https://your.domain/Dashboard/integration_dashboard.html`.

## 4) Požarni zid in omejitve
- Odpri le 80/443 (ali tunelske porte), **zapri 5002/8082** za javni internet.
- Omeji dostop na svoje IP-je (ufw/nftables) ali samo na VPN interface.
- Redno rotiraj gesla in posodabljaj pakete.

## 5) Hitri checklist
- [ ] Backend teče (`start_money_server.sh`)
- [ ] Dashboard strežnik teče (`python3 -m http.server 8082 --bind 0.0.0.0`)
- [ ] Dostop prek VPN/SSH tunela ali nginx z HTTPS + basic auth
- [ ] 5002/8082 nista odprta javno
- [ ] Certifikat veljaven, gesla rotirana

Shranjeno: `/home/saba/Desktop/NET_DEPLOYMENT_INSTRUCTIONS.md`
