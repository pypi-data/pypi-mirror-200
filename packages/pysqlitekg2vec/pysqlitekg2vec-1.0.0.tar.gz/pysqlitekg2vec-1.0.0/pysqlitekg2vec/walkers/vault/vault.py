from abc import ABC, abstractmethod
from typing import Union, Iterable, List, Iterator

from sortedcontainers import SortedDict

from pysqlitekg2vec.typings import SWalk

EntityID = Union[str, int]


class WalkImporter(ABC):
    """ an importer for generated walks """

    def __init__(self):
        """ creates a new abstract walk importer. """
        self._walker_id = 0

    def set_walker_id(self, walker_id: int) -> None:
        """sets the ID of the current walker from which walks are added.

        :param walker_id: ID of the current walker from which walks are added.
        """
        self._walker_id = walker_id

    def __enter__(self) -> 'WalkImporter':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    def add_walks(self, entity_id: EntityID, walks: List[SWalk]) -> None:
        """adds generated walks of arbitrary length to this vault for the
        given entity.

        :param entity_id: id of the entity for which the walk was generated.
        :param walks: generated walks that shall be added to the vault.
        """
        raise NotImplementedError('must be implemented')

    @abstractmethod
    def count_stored_walks(self) -> int:
        """gets the number of stored walks with this importer.

        :return: the number of stored walks.
        """
        raise NotImplementedError('must be implemented')


class CorpusVault(ABC, Iterable[SWalk]):
    """ a vault of all generated walks representing the corpus. The walks have
     always been returned in the same order to keep determinism. """

    @abstractmethod
    def walk_importer(self) -> WalkImporter:
        """gets a walk importer with which generated walks can be stored to
        this vault."""
        raise NotImplementedError('must be implemented')

    def __iter__(self) -> Iterator[SWalk]:
        """returns an iterator over stored walks."""
        raise NotImplementedError('must be implemented')

    def __len__(self) -> int:
        """returns the number of stored walks."""
        raise NotImplementedError('must be implemented')

    @abstractmethod
    def free(self):
        """closes this vault and frees up resources."""
        raise NotImplementedError('must be implemented')


class _WalkIterator(Iterator[SWalk]):
    """ a iterator over the walks of an in-memory vault. """

    def __init__(self, walk_iter: Iterator[List[SWalk]],
                 *,
                 e_walks: bool = False):
        self._walk_iter = walk_iter
        self._e_walks = e_walks
        self._walk_list_iter = None

    def __next__(self) -> SWalk:
        if self._walk_list_iter is None:
            self._walk_list_iter = iter(next(self._walk_iter))
        try:
            walk = next(self._walk_list_iter)
            if self._e_walks:
                return tuple(h for i, h in enumerate(walk) if i % 2 == 0)
            else:
                return tuple(walk)
        except StopIteration:
            self._walk_list_iter = None
            return next(self)


class _InMemoryWalkImporter(WalkImporter):
    """ an importer of generated walks to an in-memory vault. """

    def __init__(self, vault: SortedDict):
        super().__init__()
        self._vault = vault
        self._n_walks = 0

    def count_stored_walks(self) -> int:
        return self._n_walks

    def add_walks(self, entity_id: EntityID, walks: List[SWalk]) -> None:
        self._vault['%s_%s' % (str(self._walker_id), str(entity_id))] = walks
        self._n_walks += len(walks)


class InMemoryCorpusVault(CorpusVault):
    """ a vault of all generated walks which are stored in memory. """

    def __init__(self, e_walks: bool = False):
        """creates a new in-memory vault.

        :param e_walks: `True`, if walks shall be extracted as e-walks, or
        `False` otherwise. It is `False` by default.
        """
        self._vault = SortedDict()
        self._e_walks = e_walks
        self._importer = _InMemoryWalkImporter(self._vault)

    def walk_importer(self) -> WalkImporter:
        return self._importer

    def __iter__(self) -> Iterator[SWalk]:
        return _WalkIterator(iter(self._vault.values()),
                             e_walks=self._e_walks)

    def __len__(self):
        return self._importer.count_stored_walks()

    def free(self):
        self._vault = None
        self._importer = None


class CorpusVaultFactory(ABC):
    """ an abstract factory to create corpus vaults of a specific type. """

    @abstractmethod
    def create(self) -> CorpusVault:
        """creates a new corpus vault.

        :return: a new corpus vault.
        """
        raise NotImplementedError('must be implemented')


class InMemoryCorpusVaultFactory(CorpusVaultFactory):
    """ a factory for creating new in-memory corpus vaults. """

    def __init__(self, e_walks: bool = False):
        """creates a new in-memory corpus vault.

        :param e_walks: `True`, if walks shall be extracted as e-walks, or
        `False` otherwise. It is `False` by default.
        """
        self._e_walks = e_walks

    def create(self) -> CorpusVault:
        return InMemoryCorpusVault(e_walks=self._e_walks)
