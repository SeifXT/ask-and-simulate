# Data directory

Keep local source data and generated extracts under this directory.

- `raw/`: downloaded source files; never commit raw data by default.
- `interim/`: intermediate transformed data; local only unless a small fixture is approved.
- `processed/`: reproducible outputs; commit only when permitted and useful.

Commit scripts, schemas, dictionaries, provenance and small approved test fixtures rather than full database dumps. Check the dataset licence and repository policy before sharing any extract.
