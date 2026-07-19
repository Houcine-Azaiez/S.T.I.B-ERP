# S.T.I.B ERP

Local Odoo Community setup for the concrete products company prototype.

## Stack

- Odoo Community via Docker image `odoo:19.0`
- PostgreSQL via Docker image `postgres:15`
- Custom modules in `custom-addons/`

## Start

```powershell
docker compose up -d
```

Open:

```text
http://localhost:8069
```

## Stop

```powershell
docker compose down
```

## Project Structure

```text
beton-odoo/
├── compose.yaml
├── config/
│   └── odoo.conf
├── custom-addons/
└── backups/
```

## Notes

- Do not edit Odoo core source code.
- Put company-specific modules in `custom-addons/`.
- Change all passwords before deploying to a real server.
- For production, add HTTPS, domain, backups, firewall, monitoring, and a separate test database.

## Seed Starter Data

After creating the local `stib_erp` database, you can create the starter product
categories and prototype products with:

```powershell
Get-Content .\scripts\seed_starter_data.py | docker exec -i beton-odoo odoo shell -d stib_erp --no-http
```
