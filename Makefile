.PHONY: all
.PHONY: favicon
.PHONY: packages
.PHONY: scripts
.PHONY: styles
.PHONY: clean

all: clean favicon packages scripts styles

clean:
	rm -rf ./built/
	rm -rf ./public/
	mkdir ./built/
	mkdir ./public/

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

