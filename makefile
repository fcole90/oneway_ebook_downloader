all: epub

pdf:
	pandoc -s Output.md -o OneWay.pdf --chapters --toc

html: Output.md
	pandoc -s Output.md -o OneWay.html --to=HTML5

epub:
	pandoc -s Output.md -o OneWay.epub --to=epub3

clean:
	rm *.pdf *.html
