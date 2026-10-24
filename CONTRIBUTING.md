# Contributions and reproducibility

This is a research portfolio repository. Suggestions, issue reports and methodological critiques are welcome.

Please keep any proposed benchmark change separate from the archived retrospective results. Do not rewrite historical evaluation scores or describe already-consulted years as independent test sets.

Do not commit raw Taiwan sensor observations, university group slides, original shared R code, UCI CSVs, access credentials or personal data. The public repository intentionally stores only derived metrics and newly authored materials.

Before opening a pull request, run:

```bash
python -m pip install -r beijing/requirements.txt
python -m unittest discover -s beijing/tests -v
```

Full-data reproduction requires obtaining the Beijing dataset independently from UCI. See [beijing/README.md](beijing/README.md). No software license has been selected yet; please ask before reusing code outside this repository.
