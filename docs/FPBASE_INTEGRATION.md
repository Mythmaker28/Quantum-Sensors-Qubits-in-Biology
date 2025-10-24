# FPbase Integration Guide
========================

## Overview

This document describes the integration of FPbase (Fluorescent Protein Database) with the Biological Qubit Atlas for version 1.3.

## FPbase API

### GraphQL Endpoint
- **URL**: `https://fpbase.org/api/graphql/`
- **License**: CC BY-SA 4.0 (pointer-only for API data)
- **Rate Limits**: 60 requests/minute, 1000 requests/hour

### Available Data Fields

#### Core Properties
- `id`: Unique FPbase identifier
- `name`: Protein name (e.g., "EGFP", "mCherry")
- `slug`: URL-friendly identifier
- `emMax`: Maximum emission wavelength (nm)
- `exMax`: Maximum excitation wavelength (nm)

#### Optical Properties
- `brightness`: Relative brightness compared to EGFP
- `quantumYield`: Quantum yield (0.0-1.0)
- `extinctionCoefficient`: Molar extinction coefficient (M⁻¹ cm⁻¹)
- `photostability`: Relative photostability

#### Physical Properties
- `pka`: pKa value
- `maturationTime`: Maturation time (hours)
- `oligomericState`: Oligomeric state (monomer/dimer/tetramer)
- `molecularWeight`: Molecular weight (Da)
- `aminoAcidLength`: Number of amino acids

#### Structure References
- `structure.pdb`: PDB ID if available
- `structure.emdb`: EMDB ID if available

#### References
- `references`: Array of scientific references with DOI/PMID

## License Compliance

### Attribution Requirements
All FPbase data must include proper attribution:
```
Data sourced from FPbase (https://fpbase.org/) under CC BY-SA 4.0 license.
```

### Usage Restrictions
- **Commercial Use**: Allowed
- **Modification**: Allowed
- **Distribution**: Allowed with attribution
- **API Data**: Pointer-only (no bulk copying of text content)

## Integration Strategy

### Data Harvesting
1. **GraphQL Queries**: Use structured queries to fetch specific protein data
2. **Rate Limiting**: Implement exponential backoff for API calls
3. **Caching**: Store snapshots locally to reduce API load
4. **Fallback**: Use seed-based harvest if FPbase is unavailable

### Data Quality Tiers
- **Tier A**: Measured values with confidence intervals
- **Tier B**: Measured values without confidence intervals  
- **Tier C**: Computed or estimated values

### Field Mapping
See `schema/fpbase_map.yaml` for complete field mappings from FPbase to Atlas schema.

## Error Handling

### API Failures
- **Retry Logic**: 3 attempts with exponential backoff
- **Timeout**: 30 seconds per request
- **Fallback**: Switch to seed-based harvest from UniProt/PDB

### Data Validation
- **Range Checks**: Validate wavelength ranges (300-1000 nm)
- **Type Validation**: Ensure numeric fields are properly typed
- **Required Fields**: Validate presence of core fields

## Implementation Status

### Current (v1.2.1)
- ✅ Stub implementation created
- ✅ GraphQL query defined
- ✅ Field mapping schema defined
- ✅ Documentation written

### Planned (v1.3)
- 🔄 Full GraphQL integration
- 🔄 Automated data harvesting
- 🔄 Quality tier assignment
- 🔄 License compliance automation

## Usage Examples

### Basic Query
```python
from scripts.etl.fetch_fpbase_graphql import fetch_fpbase_data

# Fetch first 50 proteins
result = fetch_fpbase_data(limit=50, offset=0)

if result["status"] == "success":
    proteins = result["data"]["data"]["fluorescentProteins"]["edges"]
    print(f"Retrieved {len(proteins)} proteins")
else:
    print(f"Error: {result['error']}")
```

### Field Mapping
```python
from schema.fpbase_map import field_mappings

# Map FPbase field to Atlas field
fpbase_field = "emMax"
atlas_field = field_mappings[fpbase_field]  # "emission_nm"
```

## Future Enhancements

### v1.4 Plans
- **Bulk Download**: Support for bulk data export
- **Advanced Filtering**: Filter by family, brightness, etc.
- **Real-time Updates**: Webhook integration for new proteins
- **Community Contributions**: Allow FPbase community to contribute

### Integration with Other Sources
- **UniProt**: Cross-reference FPbase IDs with UniProt entries
- **PDB**: Link structural data from FPbase to PDB entries
- **PMC**: Use FPbase references to find additional literature

## Troubleshooting

### Common Issues
1. **Rate Limiting**: Implement proper delays between requests
2. **Network Timeouts**: Use retry logic with exponential backoff
3. **Data Inconsistencies**: Validate data ranges and types
4. **License Compliance**: Ensure proper attribution in all outputs

### Support
- **FPbase Documentation**: https://fpbase.org/about/
- **GraphQL Playground**: https://fpbase.org/api/graphql/
- **GitHub Issues**: Report integration issues in the Atlas repository

## Changelog

### v1.0 (2024-01-15)
- Initial stub implementation
- GraphQL query definition
- Field mapping schema
- Documentation created

---

*This integration enables the Atlas to leverage FPbase's comprehensive fluorescent protein database while maintaining strict license compliance and data quality standards.*
