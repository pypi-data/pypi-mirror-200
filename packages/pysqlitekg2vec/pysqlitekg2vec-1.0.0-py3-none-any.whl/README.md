# What is SQLiteKG2Vec?

SQLitKG2Vec is an experimental extension of the popular pyRDF2Vec
library for training RDF2Vec embeddings. It might in the future be
merged into the main project. This experimental extension stores the
statements of the KG as well as the generated walks into a simple SQLite
database. Hence, it is possible to train embeddings for huge knowledge
graphs without running into memory issues.

RDF2Vec is an unsupervised technique that builds further on
[Word2Vec](https://en.wikipedia.org/wiki/Word2vec), where an embedding
is learned per word, in two ways:

1.  **the word based on its context**: Continuous Bag-of-Words (CBOW);
2.  **the context based on a word**: Skip-Gram (SG).

To create this embedding, RDF2Vec first creates "sentences" which can be
fed to Word2Vec by extracting walks of a certain depth from a Knowledge
Graph.

This repository contains an implementation of the algorithm in "RDF2Vec:
RDF Graph Embeddings and Their Applications" by Petar Ristoski, Jessica
Rosati, Tommaso Di Noia, Renato De Leone, Heiko Paulheim
([\[paper\]](http://semantic-web-journal.net/content/rdf2vec-rdf-graph-embeddings-and-their-applications-0)
[\[original
code\]](http://data.dws.informatik.uni-mannheim.de/rdf2vec/)).

# Getting Started

For most uses-cases, here is how `pySQLiteKG2Vec` should be used to
generate embeddings and get literals from a given Knowledge Graph (KG)
and entities:

``` python
from pyrdf2vec import RDF2VecTransformer
from pyrdf2vec.embedders import Word2Vec
from pyrdf2vec.graphs.io import open_from_pykeen_dataset
from pyrdf2vec.walkers import RandomWalker
from pyrdf2vec.walkers.vault.sqlitevault import SQLiteCorpusVaultFactory

with open_from_pykeen_dataset('dbpedia50') as kg:
    transformer = RDF2VecTransformer(
        Word2Vec(epochs=10),
        walkers=[RandomWalker(max_walks=200,
                              max_depth=4,
                              random_state=133,
                              with_reverse=False,
                              n_jobs=1)],
        vault_factory=SQLiteCorpusVaultFactory('corpus.db'),
        verbose=1
    )
    # train RDF2Vec
    ent = kg.entities()
    embeddings, _ = transformer.fit_transform(kg, ent)
    with open('embeddings.tsv', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for name, vector in kg.pack(ent, embeddings):
            writer.writerow([name] + [x for x in vector])
```

## Create from PyKeen dataset

[PyKeen](https://github.com/pykeen/pykeen) is a popular library for
knowledge graph embeddings, and it specifies a number of datasets that
are commonly referenced in scientific literature. An SQLite KG can be
constructed from a PyKeen dataset by specifying the name of the dataset
or passing the dataset instance.

In the following code snippet, the <span class="title-ref">db100k</span>
dataset, which is a subsampling of DBpedia, is used to construct an
SQLite KG.

``` python
from pyrdf2vec.graphs.io import open_from_pykeen_dataset

with open_from_pykeen_dataset('db100k', combined=True) as kg:
    # ...
    pass
```

**Parameters:**

-   *combined* - <span class="title-ref">False</span> if only the
    training set of a dataset shall be used for the training of RDF2Vec.
    <span class="title-ref">True</span> if all the sets (training,
    testing and validation) shall be used. It is <span
    class="title-ref">False</span> by default.

## Create from TSV file

In order to save memory for big knowledge graphs, it might be a good
idea to load the statements of such a knowledge graph from a TSV file
into a SQLite KG. All the rows in the TSV file must have three columns,
where the first column is the subject, the second is the predicate, and
the last column is the object.

The following code snippet creates a new SQLite KG instance from the
statements of the specified TSV file, which has been compressed using
GZIP.

``` python
from pyrdf2vec.graphs.io import open_from_tsv_file

with open_from_tsv_file('statements.tsv.gz', compression='gzip') as kg:
    # ...
    pass
```

**Parameters:**

-   *skip_header* - <span class="title-ref">True</span> if the first row
    shall be skipped, because it is a header row for example. <span
    class="title-ref">False</span> if it shouldn't be skipped. It is
    <span class="title-ref">False</span> by default.
-   *compression* - specifies the compression type of source TSV file.
    The default value is <span class="title-ref">None</span>, which
    means that the source isn't compressed. At the moment, only <span
    class="title-ref">'gzip'</span> is supported as compression type.

## Create from Pandas dataframe

A knowledge graph can be represented in a Pandas dataframe, and this
method allows to create an SQLite KG from a dataframe. While the
dataframe can have more than three columns, the three columns
representing the subject, predicate and object must be specified in this
particular order.

The following code snippet creates a new SQLite KG instance from a
dataframe.

``` python
from pyrdf2vec.graphs.io import open_from_dataframe

with open_from_dataframe(df, column_names=('subj', 'pred', 'obj')) as kg:
    # ...
    pass
```

**Parameters:**

-   *column_names* - a tuple of three indices for the dataframe, which
    can be an integer or string. The first entry of the tuple shall
    point to the subject, the second to the predicate, and the third one
    to the object. <span class="title-ref">(0, 1, 2)</span> are the
    default indices.

## Limitations

This extension has three limitations in contrast to the original
implementation.

1)  **Literals** are ignored by this implementation for now.
2)  **Samplers** (besides the default one) might not work properly.

## Installation

`pySQLiteKG2Vec` can be installed in three ways:

1.  from [PyPI](https://pypi.org/project/pySQLiteKG2Vec) using `pip`:

``` bash
pip install pySQLiteKG2Vec
```

2.  from any compatible Python dependency manager (e.g., `poetry`):

``` bash
poetry add pyRDF2vec
```

3.  from source:

``` bash
git clone https://github.com/IBCNServices/pyRDF2Vec.git
pip install .
```

# Documentation

For more information on how to use `pyRDF2Vec`, [visit our online
documentation](https://pyrdf2vec.readthedocs.io/en/latest/) which is
automatically updated with the latest version of the `main` branch.

From then on, you will be able to learn more about the use of the
modules as well as their functions available to you.

# Contributions

Your help in the development of `pyRDF2Vec` is more than welcome.

<p align="center">
  <img width="85%" src="./assets/architecture.png" alt="architecture">
</p>

The architecture of `pyRDF2Vec` makes it easy to create new extraction
and sampling strategies, new embedding techniques. In order to better
understand how you can help either through pull requests and/or issues,
please take a look at the
[CONTRIBUTING](https://github.com/IBCNServices/pyRDF2Vec/blob/main/CONTRIBUTING.rst)
file.

# FAQ

## How to Ensure the Generation of Similar Embeddings?

`pySQLiteKG2Vec`'s walking strategies, sampling strategies and Word2Vec
work with randomness. To get reproducible embeddings, you firstly need
to **use a seed** to ensure determinism:

``` bash
PYTHONHASHSEED=42 python foo.py
```

Added to this, you must **also specify a random state** to the walking
strategy which will implicitly use it for the sampling strategy:

``` python
from pyrdf2vec.walkers import RandomWalker

RandomWalker(2, None, random_state=42)
```

**NOTE:** the `PYTHONHASHSEED` (e.g., 42) is to ensure determinism.

Finally, to ensure random determinism for Word2Vec, you must **specify a
single worker**:

``` python
from pyrdf2vec.embedders import Word2Vec

Word2Vec(workers=1)
```

**NOTE:** using the `n_jobs` and `mul_req` parameters does not affect
the random determinism.

## Why the Extraction Time of Walks is Faster if `max_walks=None`?

Currently, **the BFS function** (using the Breadth-first search
algorithm) is used when `max_walks=None` which is significantly
**faster** than the DFS function (using the Depth-first search
algorithm) **and extract more walks**.

We hope that this algorithmic complexity issue will be solved for the
next release of `pyRDf2Vec`

## How to Silence the tcmalloc Warning When Using FastText With Mediums/Large KGs?

Sets the `TCMALLOC_LARGE_ALLOC_REPORT_THRESHOLD` environment variable to
a high value.

# Referencing

If you use `pyRDF2Vec` in a scholarly article, we would appreciate a
citation:

``` bibtex
@article{pyrdf2vec,
  title        = {pyRDF2Vec: A Python Implementation and Extension of RDF2Vec},
  author       = {Vandewiele, Gilles and Steenwinckel, Bram and Agozzino, Terencio and Ongenae, Femke},
  year         = 2022,
  publisher    = {arXiv},
  doi          = {10.48550/ARXIV.2205.02283},
  url          = {https://arxiv.org/abs/2205.02283},
  copyright    = {Creative Commons Attribution 4.0 International},
  organization = {IDLab},
  keywords     = {Machine Learning (cs.LG), FOS: Computer and information sciences, FOS: Computer and information sciences}
}
```
