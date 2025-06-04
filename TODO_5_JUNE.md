# Arbetsplan 5 Juni

## Nuläge (Status)
1. Databas Status ✅
   - Alla tabeller är skapade:
     * `banks` (0 rader)
     * `customers` (0 rader)
     * `accounts` (0 rader)
     * `transactions` (0 rader)
   - Alla constraints är på plats:
     * Kontonummer: `SE8902[A-Z]{4}\d{14}`
     * Personnummer: `\d{6}-\d{4}`
     * Telefonnummer: `\+46\s*\(\d{1,4}\)\s*\d{3}\s*\d{2}\s*\d{2}`
     * Postnummer: `\d{5}`
   - Alla relationer är uppsatta:
     * Kunder → Bank
     * Konton → Kund
     * Transaktioner → Konto

## Prioritet 1: Data Import & Validering
1. Verifiera CSV-data 🔄
   - Kontrollera att CSV-filerna finns
   - Verifiera dataformat
   - Kör initial validering

2. Kör Workflow för Import 🔄
   - Validera data genom workflow
   - Importera till databasen
   - Verifiera att data har importerats korrekt

3. Testa Constraints 🔄
   - Verifiera att alla constraints fungerar
   - Testa felhantering
   - Dokumentera eventuella valideringsfel

## Prioritet 2: Presentation Förberedelse
1. Förbereda workflow demonstration
   - Visa dataflödet: CSV → Validering → Databas
   - Demonstrera Prefect workflow
   - Visa valideringsresultat
   - Visa data i databasen

2. Sammanställa presentation
   - Visa datakvalitetsproblem vi hittade:
     * 419 duplicate personnummer
     * 55 underage customers
     * 998 invalid postal codes
     * 886 invalid cities
     * 459 non-standard phone numbers
   - Visa hur vi löste problemen
   - Visa prestanda med nuvarande data

## Prioritet 3: Individuell Dokumentation
1. Skriva individuell analys
   - Beskriva datakvalitetsproblemen
   - Förklara våra lösningar
   - Reflektera över samarbetet
   - Dokumentera lärdomar

## Tidplan
- 09:00-10:30: Data Import & Validering
- 10:30-12:00: Verifiera databasen
- 13:00-14:30: Presentation förberedelse
- 14:30-16:00: Individuell dokumentation 