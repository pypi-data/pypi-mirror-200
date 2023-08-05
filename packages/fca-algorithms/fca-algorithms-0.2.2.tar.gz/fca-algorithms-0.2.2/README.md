# FCA algorithms

This is a module providing a set of commonly used algorithms in FCA, RCA, and some of its variants. Its general intention is to provide an easy to use API so that it's easier to create other programs using these algorithms. Since it's built with python, the overall performance is not expected to be outstanding. Having that said, the chosen algorithms have a somewhat low algorithmic temporal complexity.


# CLI


## FCA

### Plot a hasse diagram from a context

```bash
fca_cli -c input.csv --show_hasse
```

The context is expected to be a `csv` with the following format

name|attr1|attr2
----|:-----:|:-----:
obj1|x|
obj2||x
obj3|x|x
obj4||


### Output files

```bash
fca_cli -c input.csv --show_hasse --output_dir path/to/folder/ 
```

Will create two files, one representing the hasse graph, the other one with a concept for each line. The line is the index in the hasse graph.

## RCA

To plot the hasse diagrams of the contexts 1 and 2 after applying RCA with exists

```bash
fca_cli -k context_1.csv context_2.csv -r relation_1_2.csv relation_2_1.csv --show_hasse
```

to specify operator

```bash
fca_cli -k context_1.csv context_2.csv -r relation_1_2.csv relation_2_1.csv --show_hasse -o forall
```


# FCA utils

Module for FCA basics such as retrieving concepts, drawing a hasse diagram, etc

## Getting formal concepts

```python
from fca.api_models import Context

c = Context(O, A, I)
concepts = c.get_concepts(c)
```

## Getting association rules


```python
from fca.api_models import Context

c = Context(O, A, I)
c.get_association_rules(min_support=0.4, min_confidence=1)
```


## Drawing hasse diagram


```python
from fca.plot.plot import plot_from_hasse
from fca.api_models import Context


c = Context(O, A, I)
hasse_lattice, concepts = c.get_lattice(c)
plot_from_hasse(hasse_lattice, concepts)
```

# TODO

- Make algorithms to be able to work with streams (big files)


# Contributors

* Ramshell (Nicolas Leutwyler)
