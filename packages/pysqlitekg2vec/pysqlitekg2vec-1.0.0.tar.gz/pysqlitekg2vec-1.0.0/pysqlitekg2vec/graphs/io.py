import csv
import gzip

from io import TextIOWrapper
from typing import TYPE_CHECKING, Iterable, Sequence, Union, Tuple, Hashable

from pysqlitekg2vec.graphs.sqlite.sqlitekg import SQLiteKG, AutoLoadableSQLiteKG

if TYPE_CHECKING:
    from pandas import DataFrame
    from pykeen.datasets import Dataset
    from pykeen.triples import TriplesFactory
    from os import PathLike

FilePath = Union[str, 'PathLike[str]']
PyKeenTriplesFactory = Union['TriplesFactory', Sequence['TriplesFactory']]
ColumnSelection = Tuple[Hashable, Hashable, Hashable]
Triple = Union[Tuple[str, str, str], Sequence[str]]


class TSVReader:
    """ a reader of TSV files, which can also be compressed """

    compression_map = {
        'gzip': lambda x: gzip.open(x, mode='rt')
    }

    def __init__(self, f: Union[FilePath, TextIOWrapper],
                 compression: str = None):
        """ creates a new reader for the specified source. If the source is
        compressed, then the compression type can be specified. Per default, it
        is assumed that the source isn't compressed.

        :param f: the source to read the TSV data from.
        :param compression: the type of compression used for the TSV file.
        `None` per default, which means no compression.
        """
        if compression is None:
            self._source = f
        elif compression in self.compression_map:
            self._source = self.compression_map[compression](f)
        else:
            raise ValueError('the compression type "%s" isn\'t supported'
                             % compression)

    def __enter__(self) -> Iterable[Sequence[str]]:
        return csv.reader(self._source, delimiter='\t')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self._source, 'read'):
            self._source.__exit__(exc_type, exc_val, exc_tb)


def open_from_pykeen_dataset(dataset: Union[str, 'Dataset'],
                             *,
                             combined: bool = False,
                             **kwargs) -> SQLiteKG:
    """ constructs a new SQLiteKG instance from PyKeen dataset using the
    specified file path to persist the KG on disk. The PyKeen dataset can either
    be a name or a dataset instance.

    :param dataset: name of the dataset or an instance of Pykeen dataset class.
    :param combined: `True`, if the whole dataset (training, testing and
    validation set) shall be used, or `False`, if only the training set shall be
    used. It is `False` per default.
    :return: a new SQLiteKG instance for the given KG.
    """
    from pykeen.datasets import get_dataset

    ds = get_dataset(dataset=dataset) if isinstance(dataset, str) else dataset
    if combined:
        return open_from_triples_factory([ds.training, ds.testing,
                                          ds.validation], **kwargs)
    else:
        return open_from_triples_factory([ds.training], **kwargs)


def open_from_triples_factory(triples_factories: PyKeenTriplesFactory,
                              **kwargs) -> SQLiteKG:
    """ constructs a new SQLiteKG instance from PyKeen triples factories using
    the specified file path to persist the KG on disk. A PyKeen triples factory
    can either be a single instance or a sequence.

    :param triples_factories: a single instance or a sequence of triple factory.
    :return: a new SQLiteKG instance for the given KG.
    """

    def iterate():
        yield_triples = set()
        for tf in triples_factories:
            for triple in tf.label_triples(tf.mapped_triples):
                t = (triple[0], triple[1], triple[2])
                if t not in yield_triples:
                    yield_triples.add(t)
                    yield t

    return open_from(iterate(), **kwargs)


def open_from_tsv_file(f: Union[FilePath, 'TextIOWrapper'],
                       *,
                       skip_header: bool = False,
                       compression: str = None,
                       **kwargs) -> SQLiteKG:
    """ constructs a new SQLiteKG instance from the given TSV file using the
    specified file path to persist the KG on disk.

    :param f: source of the TSV file.
    :param skip_header: if the header shall be skipped. `False` per default.
    :param compression: the compression type of the TSV source. `None` per
    default.
    :return: a new SQLiteKG instance for the given KG.
    """

    def iterate():
        with TSVReader(f, compression=compression) as reader:
            it = iter(reader)
            try:
                if skip_header:
                    # ignore first row
                    next(it)
                while True:
                    row = next(it)
                    if len(row) != 3:
                        raise ValueError(
                            'triple must have exactly three entries, but has %d'
                            % len(row))
                    yield row[0], row[1], row[2]
            except StopIteration:
                pass

    return open_from(iterate(), **kwargs)


def open_from_dataframe(data: 'DataFrame',
                        *,
                        column_names: ColumnSelection = (0, 1, 2),
                        **kwargs) -> SQLiteKG:
    """ constructs a new SQLiteKG instance from the given pandas dataframe using
    the specified file path to persist the KG on disk.

    :param data: pandas dataframe containing all the triples representing the
    KG.
    :param column_names: the column name of subject, predicate and object in
    the given dataframe. It must be specified as a tuple (size 3) of strings or
    integers.
    :return: a new SQLiteKG instance for the given KG.
    """

    def iterate():
        for _, row in data.iterrows():
            t = []
            for i in range(0, 3):
                if column_names[i] not in row:
                    raise ValueError(
                        'column with name "%s" not in given dataframe'
                        % column_names[i])
                t.append(str(row[column_names[i]]))
            yield t[0], t[1], t[2]

    return open_from(iterate(), **kwargs)


def open_from(data: Iterable[Triple],
              *,
              skip_verify: bool = False,
              skip_predicates: Iterable[str] = None,
              db_file_path: str = 'tmp.db',
              **kwargs) -> SQLiteKG:
    """ constructs a new SQLiteKG instance with the given data using the
    specified file path to persist the KG on disk.

    :param data: an iterable sequence of triples representing the KG.
    :param skip_verify: `False`, if it shall be checked whether the
    specified list of entities (for training) are actually part of this
    knowledge graph. Otherwise, it is `True`. It is `False` by default.
    :param skip_predicates: a list of predicates, which makes all the
    statements with one of these predicates to be ignored.
    :param db_file_path: path to the file that shall hold the KG on disk.
    :return: a new SQLiteKG instance for the given KG.
    """

    def iterate():
        for t in data:
            if len(t) != 3:
                raise ValueError(
                    'triple must have exactly three entries, but has %d'
                    % len(t))
            yield t[0], t[1], t[2]

    return AutoLoadableSQLiteKG(iterate(), db_file_path,
                                skip_verify=skip_verify,
                                skip_predicates=skip_predicates,
                                **kwargs)
