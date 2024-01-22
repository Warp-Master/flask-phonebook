# Deploy
1. clone this repo
2. cd into project directory
3. `cp example.env .env`
4. Edit `.env` for your needs
5. `docker compose up -d`
6. Now app available on `$APP_PORT` port, pgadmin available on `$PGADMIN_PORT` port
7. If necessary, set up reverse proxy, configure domain and TLS certificates. Open ports in firewall
8. Keep in mind that all data stored in db container without additional configuration
