# Projektstruktur och Workflow

## Aktiva Komponenter

### 1. Datakvalitetsvalidering
* [`notebooks/data_quality_validation.ipynb`](../notebooks/data_quality_validation.ipynb)
  - Huvudnotebook för datakvalitetsvalidering
  - Visualiseringar och statistik
  - Pandas-baserad dataanalys

* [`notebooks/transaction_validation.ipynb`](../notebooks/transaction_validation.ipynb)
  - Great Expectations implementation
  - Validering av transaktioner
  - Automatiserade kvalitetskontroller

### 2. Databehandling och Workflow
* [`src/data_processing/workflow.py`](../src/data_processing/workflow.py)
  - Prefect workflow orchestrering
  - Koordinerar datainläsning, validering och export
  - Felhantering och loggning

* [`src/data_processing/transaction_validator.py`](../src/data_processing/transaction_validator.py)
  - Validering av transaktioner
  - Belopps- och valutakontroller
  - Frekvens- och limitkontroller

* [`src/data_processing/data_validator.py`](../src/data_processing/data_validator.py)
  - Validering av kunddata
  - Personnummer- och adressvalidering
  - Format- och innehållskontroller

* [`src/data_processing/customer_data_analyzer.py`](../src/data_processing/customer_data_analyzer.py)
  - Analys av kunddata
  - Rapportgenerering
  - Statistik och mönsteridentifiering

### 3. Databashantering
* [`src/models/database_models.py`](../src/models/database_models.py)
  - SQLAlchemy databasmodeller
  - Schema och relationer
  - Databasvalidering

* [`src/models/__init__.py`](../src/models/__init__.py)
  - Moduldefinitioner
  - Export av databasmodeller

### 4. Övervakning och Loggning
* [`src/utils/monitoring.py`](../src/utils/monitoring.py)
  - Loggning av valideringsresultat
  - Övervakning av dataflöden
  - Felrapportering

## Workflow Process

1. **Datainläsning**
   - Läser CSV-filer med transaktions- och kunddata
   - Hanteras av Prefect workflow

2. **Validering**
   - Great Expectations validering i notebooks
   - Detaljerad validering genom validator-klasserna
   - Automatisk felidentifiering

3. **Databashantering**
   - SQLAlchemy-modeller för databasinteraktion
   - Transaktionshantering med rollback
   - Databasvalidering

4. **Övervakning**
   - Kontinuerlig loggning
   - Resultatrapportering
   - Felhantering

## Användning

1. Kör notebooks för initial datavalidering
2. Använd Prefect workflow för automatiserad process
3. Kontrollera resultat via monitoring-systemet

## TODO: Projektstruktur Upprensning
Efter att projektet är klart ska följande filer flyttas till `src/legacy/`:

### Från startprojektet (oanvända filer):
```
src/models/
├── customer.py          - Gammal kundhantering
├── transaction.py       - Gammal transaktionshantering
├── bank.py             - Gammal bankhantering
└── account.py          - Gammal kontohantering

src/utils/
├── officer.py          - Oanvänd banktjänstemannakod
├── manager.py          - Oanvänd bankchefskod
└── interest.py         - Oanvänd ränteberäkning
```

### Överflödiga filer:
```
src/
└── check_tables.py     - Ersatt av våra valideringar
```

OBS: Denna flyttning ska göras som ett separat steg efter att projektet är klart och testat, för att undvika att bryta någon funktionalitet under utvecklingen. 