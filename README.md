1998 version of the ACM Computing Classification System (CCS),
with a small cybernetics add-on from the University of Oslo Informatics Library.

### Sources

- `src/ccs1998.txt`: *The ACM Computing Classification System (1998)* from
  https://web.archive.org/web/20120308005757/http://www.acm.org/about/class/ccs98-html

- `src/cybernetics.txt`: Cybernetics add-on from
  https://www.ub.uio.no/fag/naturvitenskap-teknologi/informatikk/emnesok/syst-oe.html

### Building

The Turtle version is build using [doit](https://pydoit.org/).

1. Run `pip install -r requirements.txt` to install dependencies.
2. Run `doit build` to build RDF versions from the TXT sources.
