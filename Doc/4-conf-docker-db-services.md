# Conf Docker DB Services

1. The container in `Docker` must listen on `0.0.0.0` (during development?). In the `docker-desktop` environment, access
   the `IPv4` address in `Windows Wireless LAN`.

2. The relevant ports for WSL firewall must be open; otherwise, the connection will fail.

3. When connecting remotely via the GUI of various database tools, enter the corresponding username and password. The IP
   address is the same as the `IP` in `1`.

4. When writing related `services`, use the connection configuration in `.env.*(dev/prod)` to avoid exposing
   information. For connection instructions, see `scripts/` or use `docker compose --help`.

5. When using database services, `voulme` mappings must be configured; otherwise, data will not be persistent and will
   be deleted every time the service is deployed.

6. Python services can be used outside the local `dev` phase initially; ensure consistency during deployment.

7. Migrations are generally unnecessary unless for educational purposes. SQL tables should be reviewed by the DBA
   beforehand.

8. Developers are prohibited from using migrations without authorization; therefore, migrations are essentially
   meaningless.