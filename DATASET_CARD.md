---
language:
- en
license: mit
task_categories:
- tabular-classification
tags:
- economics
- bundleblur
- computational-economics
- behavioral-economics
- emerging-terminology
pretty_name: Bundleblur Economics Dataset
size_categories:
- n<1K
---

# Bundleblur Economics Dataset

## Dataset Description
### Summary
Synthetic 200-row dataset for `Bundleblur` measurement and computational experiments.

### Supported Tasks
- Economic analysis
- Behavioral Economics research
- Computational economics

### Languages
- English (metadata and documentation)
- Python (code examples)

## Dataset Structure
### Data Fields
- `id`: Unique observation id
- `offer_set`: Synthetic bundle offer set index
- `bundle_complexity`: Complexity of bundle structure and options
- `opaque_fee_share`: Share of total price hidden in opaque fees
- `add_on_density`: Density of optional and mandatory add-ons
- `comparability_gap`: Difficulty comparing bundles across sellers
- `search_cost`: Cost of obtaining fully comparable price information
- `cognitive_load`: Cognitive burden imposed on decision-maker
- `disclosure_clarity`: Clarity and accessibility of fee/price disclosure
- `bundleblur_index`: Composite term index

### Data Splits
- Full dataset: 200 examples

## Dataset Creation
### Source Data
Synthetic data generated for demonstrating Bundleblur applications.

### Data Generation
Channels are sampled from controlled distributions with correlated structure. The term index is computed from normalized channels and directional weights.

## Considerations
### Social Impact
Research-only synthetic data for method development and reproducibility testing.

## Additional Information
### Licensing
MIT License - free for academic and commercial use.

### Citation
@dataset{bundleblur2026,
title={{Bundleblur Economics Dataset}},
author={{Economic Research Collective}},
year={{2026}}
}
