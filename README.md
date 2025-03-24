# Introduction

This extends the GPT-2 model by training it on economics data.

# SKIP: Preparing training data

Scrape PDFs.

```bash
./scrape.py
```

Also get PDFs from:
https://open.umn.edu/opentextbooks/subjects/economics

Convert the PDFs to a single text file.

```bash
./toText.sh
```

Encode the text file.

```bash
./encode.sh
```
