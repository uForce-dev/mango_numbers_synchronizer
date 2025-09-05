# Mango Numbers Synchronizer

Service that syncs Mango Office phone numbers to PostgreSQL.

## Features

- Create new records
- Update existing records while preserving extra user-added columns
- Logging and error handling

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` from `env.dist` and fill values:
```bash
cp env.dist .env
```

Required variables:
```env
MANGO_API_KEY=...
MANGO_SALT=...
MANGO_API_URL=https://app.mango-office.ru/vpbx/trunks/numbers
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=mango_numbers
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
LOG_LEVEL=INFO
```

## Usage

Run sync:
```bash
python main.py
```

Cron example (every 15 minutes):
```bash
*/15 * * * * cd /path/to/mango_numbers_synchronizer && python main.py
```

## Database schema

Table `phone_numbers` is created automatically with columns:
- `line_id` INTEGER PRIMARY KEY
- `number` VARCHAR(20) UNIQUE
- `name` VARCHAR(255) NULL
- `comment` TEXT NULL
- `region` VARCHAR(10)
- `schema_id` INTEGER
- `schema_name` VARCHAR(255)
- `created_at` TIMESTAMP
- `updated_at` TIMESTAMP

## Project structure

```
mango_numbers_synchronizer/
├── main.py
├── config.py
├── models.py
├── mango_client.py
├── database.py
├── sync_service.py
├── requirements.txt
├── env.dist
└── README.md
```