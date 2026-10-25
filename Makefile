.PHONY: all
.PHONY: all_except_get_text
.PHONY: get_text
.PHONY: favicon
.PHONY: packages
.PHONY: scripts
#.PHONY: styles
.PHONY: clean
.PHONY: vendor
.PHONY: vendor_nodejs
.PHONY: vendor_python
.PHONY: lock
.PHONY: lock_nodejs
.PHONY: lock_python
.PHONY: install
.PHONY: install_nodejs
.PHONY: install_python


VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python

all_except_get_text: clean favicon packages scripts

all: clean get_text favicon packages scripts

lock: lock_nodejs lock_python

lock_python:
	uv pip compile --upgrade --python-version 3.11 requirements.in --universal --generate-hashes --output-file requirements.txt
	uv pip compile --upgrade --python-version 3.11 requirements.in requirements-dev.in --universal --generate-hashes --output-file requirements-dev.txt

# Reads package.json
# Writes pnpm-lock.yaml, and also raises the minimum versions in package.json (e.g. ^9.39.5 -> ^9.40.0)
lock_nodejs:
	npx --yes pnpm@10.33.0 update

vendor: vendor_nodejs vendor_python

vendor_python:
	uv venv --clear --python 3.11 --seed $(VENV_DIR)
	$(PYTHON) -m pip download -r requirements.txt -d vendor/dist
	$(PYTHON) -m pip download -d vendor/dist pip setuptools wheel
	$(PYTHON) -m pip download -r requirements-dev.txt -d vendor/dist_dev
	$(PYTHON) -m pip download -d vendor/dist_dev pip setuptools wheel

# Downloads every package listed in pnpm-lock.yaml into vendor/pnpm-store/, so "make install" can install offline.
# Reads pnpm-lock.yaml only: doesn't change it, and doesn't look at package.json.
#   mkdir      - create vendor/npm/pnpm_tgz/ to hold the pnpm download
#   npm pack   - download pnpm 10.33.0 itself as a .tgz file into vendor/npm/pnpm_tgz/
#   npm install - unpack that .tgz into vendor/npm/pnpm_bin/, giving a local pnpm at vendor/npm/pnpm_bin/bin/pnpm
#   pnpm config set store-dir - tell that pnpm to save downloaded packages in vendor/pnpm-store/
#   pnpm fetch - read pnpm-lock.yaml and download every package it lists into vendor/pnpm-store/
vendor_nodejs:
	mkdir -p vendor/npm/pnpm_tgz
	npm pack pnpm@10.33.0 --pack-destination vendor/npm/pnpm_tgz
	npm install -g ./vendor/npm/pnpm_tgz/pnpm-10.33.0.tgz --prefix ./vendor/npm/pnpm_bin/
	./vendor/npm/pnpm_bin/bin/pnpm config set store-dir vendor/pnpm-store
	./vendor/npm/pnpm_bin/bin/pnpm fetch

clean:
	rm -rf ./built/
	rm -rf ./public/
	mkdir ./built/
	mkdir ./public/

get_text:
	python getText/scrape.py
	./getText/toText.sh
	python getText/clean.py
	./getText/merge.sh

favicon:
	cp -R ./src/img/compiled/. ./public

packages:
	mkdir ./public/packages/
	cp -R ./node_modules/bootstrap/dist/. ./public/packages/bootstrap
	#cp -R ./node_modules/jquery/dist/. ./public/packages/jquery

scripts:
	mkdir ./public/js/
	cp -R ./src/js/. ./public/js
      
#styles:
#	mkdir ./public/css/
#	cp -R./src/styles/. ./public/css
install: install_python install_nodejs
	
install_python:
	uv pip sync requirements-dev.txt --find-links vendor/dist_dev --offline --no-index
install_nodejs:
	./vendor/npm/pnpm_bin/bin/pnpm install --offline --frozen-lockfile

