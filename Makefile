.PHONY: all
.PHONY: all_except_get_text
.PHONY: get_text
.PHONY: favicon
.PHONY: packages
.PHONY: scripts
.PHONY: styles
.PHONY: clean

all_except_get_text: clean favicon packages scripts styles

all: clean get_text favicon packages scripts styles

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
	cp ./src/img/compiled/* ./public/

packages:
	mkdir ./public/packages/
	cp -R ./node_modules/bootstrap/dist ./public/packages/bootstrap
	cp -R ./node_modules/jquery/dist ./public/packages/jquery

scripts:
	#mkdir ./public/js/
	cp -R ./src/js ./public/js
      
styles:
	mkdir ./public/css/
	cp -R./src/styles/**/*.css ./public/css/ || true

