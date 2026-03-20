# Checking for updates

Rendered projects include `scripts/copier-check-update.sh` to run `copier check-update` for each `.yml` answer file in `.copier-answers/`.

From the root of a rendered project:

```bash
bash scripts/copier-check-update.sh
```

This script iterates over `.yml` files directly under `.copier-answers/` (not recursively) and runs:

```bash
copier check-update --answer-file "${answer_file}"
```

If updates are available and you want to apply them, run `copier update` with the same answer file, for example:

```bash
copier update --trust --answers-file ".copier-answers/project.yml"
```
