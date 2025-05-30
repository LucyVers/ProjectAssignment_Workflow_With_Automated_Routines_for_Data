# Regulatory Documentation

## Purpose
This directory contains official regulatory documents and sources that form the basis for my data quality validation rules. All rules and thresholds in my system must be traceable to these official sources to ensure compliance and accuracy.

## Directory Structure

```
regulatory_documents/
├── README.md                    # This file
├── sources.md                   # List of all sources with metadata
├── fi_kundkannedom_2024.pdf    # FI's customer due diligence requirements
└── fi_penningtvatt_2024.pdf    # FI's anti-money laundering regulations
```

## Document Management

### Adding New Documents
1. Download only from official sources (FI, SCB, etc.)
2. Update sources.md with metadata
3. Add reference to relevant validation rules

### Updating Documents
1. Keep track of document versions
2. Note any changes that affect our validation rules
3. Update our rules accordingly

## Usage
- Reference these documents when creating or modifying validation rules
- Each rule should cite specific sections from these documents
- Regular review to ensure continued compliance

## Maintenance
- Quarterly review of document currency
- Update when new regulations are published
- Archive outdated versions with clear documentation of changes 