# Databasinstruktioner

Detta är instruktioner för att återskapa databasen för projektet.

## Förutsättningar

- PostgreSQL 16.4 eller senare
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

### Kunder (customers)
- Personnummer
- Namn
- Kontaktinformation (telefon, adress)

### Konton (accounts)
- Kontonummer
- Kontotyp
- Koppling till kund

### Transaktioner (transactions)
- Transaktions-ID
- Belopp och valuta
- Koppling till konto
- Tidsstämpel och status

### Banker (banks)
- Banknamn
- Banknummer

## Testdata

Dump-filen innehåller testdata som tillhandahållits av kursledningen för att demonstrera systemets funktionalitet. Datan inkluderar:
- Ett urval av testkunder
- Olika kontotyper
- Transaktioner med varierande belopp och valutor

## Versionshantering

Databasen använder Alembic för versionshantering av databasschema. Detta säkerställer att alla databasändringar är spårbara och kan återställas vid behov. 