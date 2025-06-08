# Databasinstruktioner

Detta är instruktioner för att återskapa databasen för projektet.

## Förutsättningar

- PostgreSQL installerat
- Tillgång till en PostgreSQL-server
- Konfigurerad `.env`-fil baserad på `.env.example`

## Återställa databasen

1. Skapa en ny databas:
```bash
createdb bank_db
```

2. Återställ data från dump-filen:
```bash
psql -d bank_db < database_dump.sql
```

## Databasstruktur

Databasen innehåller följande huvudtabeller:
- Transaktioner
- Konton
- Kunder

## Testdata

Dump-filen innehåller testdata som behövs för att demonstrera systemets funktionalitet. 