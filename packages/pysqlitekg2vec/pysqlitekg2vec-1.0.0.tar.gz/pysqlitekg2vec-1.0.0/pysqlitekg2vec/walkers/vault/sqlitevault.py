import logging
import sqlite3
from os import remove
from os.path import exists
from sqlite3 import connect, Connection
from typing import List, Iterator, Sequence, Tuple

from pysqlitekg2vec.typings import SWalk
from pysqlitekg2vec.walkers.vault.vault import CorpusVault, EntityID, \
    CorpusVaultFactory, WalkImporter


class _DBWriteCmd:
    """ a class that maintains write commands for the SQLite database. """

    CREATE_WALK_TABLE = '''
        CREATE TABLE corpus (
            walker_id INTEGER NOT NULL,
            entity_id TEXT NOT NULL,
            walk_no INTEGER NOT NULL,
            hop_no INTEGER NOT NULL,
            hop_id TEXT NOT NULL,
            PRIMARY KEY (walker_id, entity_id, walk_no, hop_no)
        );
        '''
    CREATE_METADATA_TABLE = '''
        CREATE TABLE metadata (
            id INTEGER PRIMARY KEY DEFAULT 0,
            number_of_walks INTEGER NOT NULL,
            max_walk_length INTEGER NOT NULL
        );
        '''
    INSERT_WALK = '''
        INSERT INTO corpus (walker_id, entity_id, walk_no, hop_no, hop_id)
        VALUES (?, ?, ?, ?, ?);
        '''
    INSERT_METADATA = '''
        INSERT INTO metadata (id, number_of_walks, max_walk_length)
        VALUES (?, ?, ?);
        '''


class _DBReadCmd:
    """ a class that maintains query commands for the SQLite database. """

    WALKS_FETCH = '''
        SELECT walker_id, entity_id, walk_no, hop_no, hop_id
        FROM corpus
        ORDER BY walker_id, entity_id, walk_no, hop_no;
        '''

    COUNT_WALKS = '''SELECT number_of_walks FROM metadata WHERE id = 0;'''


class _DBRowIterator(Iterator[SWalk]):
    """ an iterator over the walks stored in vault DB. """

    def __init__(self, con: Connection, e_walks: bool = False):
        """creates a new DB iterator over the vault DB.

        :param con: of the SQLite database.
        :param e_walks: `True`, if e-walks shall be returned, otherwise
        `False`. By default, it is `False`.
        """
        self._cursor = con.cursor()
        self._e_walks = e_walks
        self._it = self._cursor.execute(_DBReadCmd.WALKS_FETCH)
        self._last_hop = None

    def _prepare_walk(self, walk: Sequence[str]) -> Tuple[str, ...]:
        """prepares the walk to be returned. This iterator can be
        configured to generate e-walks instead of regular walks.

        :param walk: the walk that shall be prepared to be returned.
        """
        if self._e_walks:
            return tuple(h for i, h in enumerate(walk) if i % 2 == 0)
        else:
            return tuple(walk)

    def __next__(self) -> SWalk:
        walk: List[str] = []
        try:
            wid, eid, wno, hop_no, hop_id = next(self._it) if \
                self._last_hop is None else self._last_hop
            walk.append(hop_id)
            while True:
                nh_wid, nh_eid, nh_wno, nh_no, nh_hid = next(self._it)
                if wid == nh_wid and eid == nh_eid and wno == nh_wno:
                    walk.append(nh_hid)
                else:
                    self._last_hop = (nh_wid, nh_eid, nh_wno, nh_no, nh_hid)
                    return self._prepare_walk(walk)
        except StopIteration as e:
            if walk:
                self._last_hop = None
                return self._prepare_walk(walk)
            self._cursor.close()
            raise e


class _SQLiteWalkImporter(WalkImporter):
    """ a walk importer into SQLite vault. """

    @staticmethod
    def _create_schema(con: Connection):
        """creates a table schema for storing generated walks.

        :param con: connection of the SQLite database in which the new tale
        shall be created.
        """
        cursor = con.cursor()
        try:
            cursor.execute(_DBWriteCmd.CREATE_WALK_TABLE)
            cursor.execute(_DBWriteCmd.CREATE_METADATA_TABLE)
        finally:
            cursor.close()

    def __init__(self, con: Connection, buffer_size: int):
        super().__init__()
        self._buffer_size = buffer_size
        self._con = con
        self._n = 0
        self._walk_count = 0
        self._max_walk_len = 0

    def __enter__(self):
        self._create_schema(self._con)
        self._con.commit()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self._con.commit()
            self._insert_metadata()

    def _insert_metadata(self):
        cursor = self._con.cursor()
        try:
            cursor.execute(_DBWriteCmd.INSERT_METADATA,
                           (0, self._walk_count, self._max_walk_len))
            self._con.commit()
        finally:
            cursor.close()

    def add_walks(self, entity_id: EntityID, walks: List[SWalk]) -> None:
        cursor = self._con.cursor()
        try:
            for walk_no, walk in enumerate(walks):
                if self._max_walk_len < (len(walk) - 1):
                    self._max_walk_len = len(walk) - 1
                for hop_no, hop_id in enumerate(walk):
                    cursor.execute(_DBWriteCmd.INSERT_WALK,
                                   (self._walker_id, str(entity_id),
                                    walk_no, hop_no, hop_id))
                    self._n += 1
                self._walk_count += 1
            if (self._n % self._buffer_size) == 0:
                self._con.commit()
        finally:
            cursor.close()

    def count_stored_walks(self) -> int:
        cursor = self._con.cursor()
        try:
            resp = cursor.execute(_DBReadCmd.COUNT_WALKS).fetchone()
            if resp is None:
                logging.warning('SQLiteKG didn\'t respond with valid walk count')
                return 0
            else:
                return int(resp[0])
        except sqlite3.Error as e:
            logging.warning('SQLiteKG couldn\'t get walk count: %s', e)
            return 0
        finally:
            cursor.close()


class _NOPSQLiteWalkImporter(_SQLiteWalkImporter):
    """  a walk importer into SQLite vault that doesn't add new walks. """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_walks(self, entity_id: EntityID, walks: List[SWalk]) -> None:
        pass


class SQLiteCorpusVault(CorpusVault):
    """ a vault of all generated walks which are stored in a single SQLite
    table. """

    def __init__(self, db_path: str,
                 *,
                 e_walks: bool = False,
                 read_only: bool = False,
                 keep_corpus: bool = False):
        """creates a new SQLite database at the given path representing the
        corpus vault.

        :param db_path: path to the database file.
        :param e_walks: `True`, if e-walks shall be returned, otherwise
        `False`. By default, it is `False`.
        :param read_only: `True`, if no schema shall be created and no walks
        shall be imported. Otherwise, `False.` By default, it is `False`.
        :param keep_corpus: `True`, if the corpus db shouldn't be deleted,
        otherwise false.
        """
        super().__init__()
        self._read_only = read_only
        self._keep_corpus = keep_corpus
        self._db_path = db_path
        self._e_walks = e_walks
        self._con = connect(db_path, check_same_thread=False)
        self._importer = _NOPSQLiteWalkImporter(self._con, 0) if \
            read_only else _SQLiteWalkImporter(self._con, 1000)

    def walk_importer(self) -> WalkImporter:
        return self._importer

    def __iter__(self) -> Iterator[SWalk]:
        return _DBRowIterator(self._con, e_walks=self._e_walks)

    def __len__(self):
        return self._importer.count_stored_walks()

    def free(self):
        if self._con is not None:
            self._con.close()
        if exists(self._db_path) and not (self._keep_corpus or
                                          self._read_only):
            remove(self._db_path)


class SQLiteCorpusVaultFactory(CorpusVaultFactory):
    """ a factory for creating new in-memory corpus vaults. """

    @staticmethod
    def _prepare_path(db_path: str) -> str:
        """checks whether the given database file already exists. If that is
        the case, then a new path is generated with a new postfix.

        :param db_path: the original path to the database.
        :return: a path for the database file that is ensured to be non
        existing.
        """
        n = 0
        new_db_path = db_path
        while exists(new_db_path):
            new_db_path = '%s_%d' % (db_path, n)
            n += 1
        return new_db_path

    def __init__(self, db_path: str,
                 *,
                 e_walks: bool = False,
                 read_only: bool = False,
                 keep_corpus: bool = False):
        """creates a new factory to create new SQLite corpus vaults.

        :param db_path: path to the database file.
        :param e_walks: `True`, if e-walks shall be returned, otherwise
        `False`. By default, it is `False`.
        :param read_only: `True`, if no schema shall be created and no walks
        shall be imported. Otherwise, `False.` By default, it is `False`.
        :param keep_corpus: `True`, if the corpus db shouldn't be deleted,
        otherwise false.
        """
        self._db_path = db_path
        self._e_walks = e_walks
        self._read_only = read_only
        self._keep_corpus = keep_corpus

    def create(self) -> CorpusVault:
        db_path = self._db_path
        if not self._read_only:
            db_path = self._prepare_path(db_path)
        return SQLiteCorpusVault(db_path,
                                 e_walks=self._e_walks,
                                 read_only=self._read_only,
                                 keep_corpus=self._keep_corpus)
