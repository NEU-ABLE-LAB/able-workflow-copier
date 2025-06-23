# `data/` Directory

Other than this `README.md` , this directory should not be committed to git.

## Directory structure

```txt
├── data/
│   ├── {{ module_name }}/
│   │   ├── external/
│   │   ├── interim/
│   │   ├── processed/
│   │   ├── raw/
│   │   └── README.md
│   ├── tests/
│   │   ├── {{ module_name }}/...
│   │   └── README.md
│   └── README.md
```

## Subdirectories

The following directories may be symlinks to other locations on disk. These target locations (instead of the relative `data/` paths) should be specified where appropriate in the `config/**/*.yml` files that specify data directories.

- **`{{ module_name }}/external`**: Data from third party sources.
- **`{{ module_name }}/interim`**: Intermediate data that has been transformed.
- **`{{ module_name }}/processed`**: The final, canonical data sets for modeling.
- **`{{ module_name }}/raw`**: The original (or validated external data), immutable data dump.
