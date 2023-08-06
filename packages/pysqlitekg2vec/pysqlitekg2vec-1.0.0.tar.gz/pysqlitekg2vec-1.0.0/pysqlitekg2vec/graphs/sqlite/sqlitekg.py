import logging

from os import remove
from os.path import exists
from sqlite3 import connect, Connection
from typing import Iterable, Tuple, List, Set, Any, Sequence, Union, \
    TYPE_CHECKING

from pysqlitekg2vec.graphs.types import EntityName, EntityID, EntityNames, \
    EntityIDs, Triple
from pysqlitekg2vec.typings import Hop, Literals, Embeddings
from pysqlitekg2vec.graphs import Vertex

from cachetools import LFUCache, cached


class _DBWriteCmd:
    """ a class that maintains write commands for the SQLite database """
    CREATE_RESOURCE_TABLE = '''
        CREATE TABLE resource(
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            iri NOT NULL UNIQUE
        );'''
    CREATE_STATEMENT_TABLE = '''
        CREATE TABLE statement(
            no INTEGER PRIMARY KEY AUTOINCREMENT,
            subj INTEGER NOT NULL,
            pred INTEGER NOT NULL,
            obj INTEGER NOT NULL,
            FOREIGN KEY (subj) REFERENCES resource (resource_id),
            FOREIGN KEY (pred) REFERENCES resource (resource_id),
            FOREIGN KEY (obj) REFERENCES resource (resource_id),
            UNIQUE(subj,pred,obj)
        ); '''
    INSERT_RESOURCE = 'INSERT INTO resource (iri) VALUES (?);'
    INSERT_STATEMENT = '''
        INSERT INTO statement (subj, pred, obj) VALUES (?, ?, ?);
        '''


class _DBQueryCmd:
    """ a class that maintains query commands for the SQLite database """
    ENTITIES_COUNT = '''
        SELECT count(*)
        FROM (SELECT subj as id
              FROM statement UNION SELECT obj as id FROM statement);
        '''
    PREDICATES_COUNT = 'SELECT count(distinct pred) FROM statement;'
    STATEMENT_COUNT_QUERY = 'SELECT count(*) FROM statement;'
    ENTITY_ID_FROM_NAME = 'SELECT resource_id FROM resource WHERE iri = ?;'
    ENTITY_NAME_FROM_ID = 'SELECT iri FROM resource WHERE resource_id = ?;'
    ALL_ENTITIES = '''
        SELECT id, iri
        FROM (SELECT subj as id FROM statement UNION
              SELECT obj as id FROM statement) entity
        JOIN resource ON entity.id = resource.resource_id;
        '''
    FETCH_HOPS = {
        'forward': 'SELECT pred, obj FROM statement WHERE subj = ?;',
        'backward': 'SELECT pred, subj FROM statement WHERE obj = ?;'
    }


class SQLiteKG:
    """ represents a Knowledge Graph persisted in a SQLite database """

    _is_remote = False

    def __init__(self, database_uri,
                 *,
                 skip_verify: bool = False):
        """ creates a new SQLite KG that connects to the database at the
        specified URI.

        :param skip_verify: `False`, if it shall be checked whether the
        specified list of entities (for training) are actually part of this
        knowledge graph. Otherwise, it is `True`. It is `False` by default.
        """
        self.skip_verify = skip_verify
        self._db_uri = database_uri
        self._con = None

    def __getstate__(self):
        return {
            'skip_verify': self.skip_verify,
            'db_uri': self._db_uri
        }

    def __setstate__(self, state):
        self.skip_verify = state['skip_verify']
        self._db_uri = state['db_uri']
        self._con = None

    @property
    def _readonly_db_uri(self):
        """ gets an SQLite URI with read-only mode for connecting to the
        specified database. """
        return self._db_uri + '?mode=ro'

    @property
    def connection(self):
        """ gets the connection to the SQLite KG database. """
        if self._con is None:
            self._con = connect(self._readonly_db_uri,
                                check_same_thread=False,
                                uri=True)
        return self._con

    @property
    def entity_count(self) -> int:
        """ count of entities (occur as subject or object) in this KG. """
        cursor = self.connection.cursor()
        try:
            return int(cursor.execute(_DBQueryCmd.ENTITIES_COUNT)
                       .fetchone()[0])
        finally:
            cursor.close()

    @property
    def predicate_count(self) -> int:
        """ count of distinct predicates in the KG. """
        cursor = self.connection.cursor()
        try:
            return int(cursor.execute(_DBQueryCmd.PREDICATES_COUNT)
                       .fetchone()[0])
        finally:
            cursor.close()

    @property
    def statement_count(self) -> int:
        """ count of statements in the KG. """
        cursor = self.connection.cursor()
        try:
            return int(cursor.execute(_DBQueryCmd.STATEMENT_COUNT_QUERY)
                       .fetchone()[0])
        finally:
            cursor.close()

    def id(self, entity_name: EntityName) -> Union[EntityID, None]:
        """ returns the integer ID of the entity in form of a string.

        :param entity_name: name of the entity for which to get the ID.
        :return: the integer ID of the entity in form of a string, or `None`,
        if no entity with such a name could be found.
        """
        cursor = self.connection.cursor()
        try:
            result = cursor.execute(_DBQueryCmd.ENTITY_ID_FROM_NAME,
                                    (entity_name,))
            entity_id_tp = result.fetchone()
            return None if entity_id_tp is None else str(entity_id_tp[0])
        finally:
            cursor.close()

    def from_id(self, entity_id: EntityID) -> Union[EntityName, None]:
        """ returns the name of the entity in form of a string.

        :param entity_id: ID of the entity for which to get the name.
        :return: the integer ID of the entity in form of a string, or `None`, if
        no entity with such a ID could be found.
        """
        cursor = self.connection.cursor()
        try:
            result = cursor.execute(_DBQueryCmd.ENTITY_NAME_FROM_ID,
                                    (int(entity_id),))
            entity_name_tp = result.fetchone()
            return None if entity_name_tp is None else entity_name_tp[0]
        finally:
            cursor.close()

    def entities(self, restricted_to: EntityNames = None) -> EntityIDs:
        """ returns all the entities, which occur as either a subject or object
        in a statement of the KG. No entity will be returned twice.

        :param restricted_to: the names (e.g. IRI) of the resources that shall
        be exclusively considered. If `None`, then all entities will be
        returned. It is `None` by default.
        :return: a list with all entity IDs.
        """
        cursor = self.connection.cursor()
        try:
            result = cursor.execute(_DBQueryCmd.ALL_ENTITIES)
            entities = [(str(row[0]), str(row[1])) for row in result]
            if restricted_to is None:
                return [e[0] for e in entities]
            else:
                restriction = set(restricted_to)
                return [e[0] for e in entities if e[1] in restriction]
        finally:
            cursor.close()

    def pack(self, entities: EntityIDs,
             embeddings: Embeddings) -> Sequence[Tuple[EntityName, str]]:
        """ packs the entities with their embeddings.

        :param entities: IDs of the entities with which the embeddings shall be
        packed.
        :param embeddings: which shall be packed with the name of the entity.
        :return: a list of the embeddings with the corresponding name of the
        entity.
        """
        if len(entities) != len(embeddings):
            raise ValueError('list of entities must be the same size as list '
                             'of embeddings')
        cursor = self.connection.cursor()
        try:
            result = cursor.execute(_DBQueryCmd.ALL_ENTITIES)
            entity_map = {int(row[0]): str(row[1]) for row in result}
            return [(entity_map[int(entityID)], embedding) for
                    entityID, embedding in zip(entities, embeddings)]
        finally:
            cursor.close()

    @staticmethod
    def _parse_hops(vertex: Vertex,
                    result: Iterable[Tuple[Any, Any]],
                    is_reverse: bool = False) -> Iterable['Hop']:
        """ parses the results from the SQL query that is fetching the direct
        hops for the specified vertex.

        :param vertex: for which the query result was returned.
        :param result: the result of the forward or backward query.
        :param is_reverse: If `True`, this function assumes that the result of
        the backward query was passed, otherwise the forward result, if `False`.
        It is `False` by default.
        :return: the extracted direct hops in proper format.
        """
        for row in result:
            other_vertex = Vertex(name=str(row[1]))
            pred = Vertex(name=str(row[0]),
                          vprev=other_vertex if is_reverse else vertex,
                          vnext=vertex if is_reverse else other_vertex,
                          predicate=True)
            yield pred, other_vertex

    @cached(cache=LFUCache(maxsize=131072))
    def get_hops(self, vertex: 'Vertex',
                 is_reverse: bool = False) -> List['Hop']:
        """ gets the direct hops of specified vertex as a list.

        :param vertex: name of the vertex for which to get the hops.
        :param is_reverse: If `True`, this function gets the parent nodes of a
        vertex (backward links). Otherwise, get the child nodes for this
        vertex (forward links). It is `False` by default.
        :return: the hops of a vertex in (predicate, object) form.
        """
        cursor = self.connection.cursor()
        try:
            link_type = 'backward' if is_reverse else 'forward'
            query = _DBQueryCmd.FETCH_HOPS[link_type]
            result = cursor.execute(query, (int(vertex.name),))
            hops = [hop for hop in self._parse_hops(vertex, result,
                                                    is_reverse)]
            logging.debug('Detected %d (%s) hops for vertex "%s"',
                          len(hops), link_type, vertex.name)
            return hops
        finally:
            cursor.close()

    def get_neighbors(self, vertex: Vertex,
                      is_reverse: bool = False) -> Set[Vertex]:
        """ gets the children or parents neighbors of a vertex.

        :param vertex: name of the vertex for which to get the neighbours.
        :param is_reverse: If `True`, this function gets the parent neighbours
        of a vertex (backward links). Otherwise, get the child neighbours for
        this vertex (forward links). It is `False` by default.
        :return: children or parents neighbors of a vertex.
        """
        cursor = self.connection.cursor()
        try:
            link_type = 'backward' if is_reverse else 'forward'
            query = _DBQueryCmd.FETCH_HOPS[link_type]
            result = cursor.execute(query, (int(vertex.name),))
            return set([pred for pred, _ in self._parse_hops(vertex,
                                                             result,
                                                             is_reverse)])
        finally:
            cursor.close()

    def get_literals(self, entities: EntityIDs, verbose: int = 0) -> Literals:
        """ gets the literals for one or more entities for all the predicates
        chain.

        :param entities: entity or entities for which to get the literals.
        :param verbose: specifies the verbosity level. `0` does not display
        anything; `1` display of the progress of extraction and training of
        walks; `2` debugging. It is `0` by default.
        :return: list that contains literals for each entity.
        """
        logging.warning('SQLiteKG doesn\'t support literals')
        return []

    def is_exist(self, entities: EntityIDs) -> bool:
        """ checks whether all provided entities exist in the KG.

        :param entities: IDs of the entities for which to check the existence.
        :return: `True`, if all the entities exists, `False` otherwise.
        """
        ent_in_kg = set([int(x) for x in self.entities()])
        for entity in entities:
            if int(entity) not in ent_in_kg:
                return False
        return True


class _Importer:
    """ importer of KG into the SQLite database """

    def __init__(self, con: Connection,
                 skip_predicates: Set[EntityName] = None):
        """ creates a new importer using the given connection. This importer
        allows to import the triples of a KG.

        :param con: connection which shall be used for the import.
        :param skip_predicates: a set of predicates, which makes all the
        statements with one of these predicates to be ignored.
        """
        self._con = con
        self._skip_predicates = skip_predicates \
            if skip_predicates is not None else set([])
        self._cursor = con.cursor()
        self._entity_map = {}

    def _create_schema(self) -> None:
        """ creates the basic schema of the SQLite database. """
        self._cursor.execute(_DBWriteCmd.CREATE_RESOURCE_TABLE)
        self._cursor.execute(_DBWriteCmd.CREATE_STATEMENT_TABLE)

    def _insert_entity(self, entity: EntityName) -> int:
        """ inserts the given entity into the database, if it doesn't already
        exist. This method returns the ID of this entity regardless of whether
        the entity was newly inserted or it already existed.

        :param entity: name of the entity that shall be inserted.
        :return: the unique integer ID of the given entity.
        """
        if entity in self._entity_map:
            return self._entity_map[entity]
        else:
            self._cursor.execute(_DBWriteCmd.INSERT_RESOURCE, (entity,))
            key = self._cursor.execute('SELECT last_insert_rowid();') \
                .fetchone()[0]
            self._entity_map[entity] = int(key)
            return key

    def import_kg(self, data: Iterable[Tuple[str, str, str]]) -> None:
        """ inserts all the statements into the database.

        :param data: a sequence of statements that shall be imported.
        """
        n = 0
        for subj, pred, obj in data:
            if pred in self._skip_predicates:
                continue
            subj_key = self._insert_entity(subj)
            pred_key = self._insert_entity(pred)
            obj_key = self._insert_entity(obj)
            self._cursor.execute(_DBWriteCmd.INSERT_STATEMENT,
                                 (subj_key, pred_key, obj_key))
            n += 1
            if n % 1000000 == 0:
                logging.info('Loaded %dM statements into SQLite KG'
                             % (n / 1000000))
        self._con.commit()
        self._create_indices()
        self._con.commit()

    def _create_indices(self) -> None:
        """create indices for faster querying."""
        self._cursor.execute(
            '''CREATE UNIQUE INDEX iri_index ON resource (iri);''')
        self._cursor.execute(
            '''CREATE INDEX subj_index ON statement (subj);''')
        self._cursor.execute('''CREATE INDEX obj_index ON statement (obj);''')

    def __enter__(self):
        self._create_schema()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self._con is not None:
                self._con.commit()
        self._entity_map = None


class AutoLoadableSQLiteKG(SQLiteKG):
    """ represents a Knowledge Graph that initially loads specified data into
     a SQLite database in a """

    def __init__(self, data: Iterable[Triple], db_file_path: str = 'tmp.db',
                 *,
                 skip_predicates: Iterable[str] = None,
                 **kwargs
                 ):
        """ creates a new auto loadable SQLite KG that persists the database in
        the specified file on disk.

        :param data: an iterable stream of triples.
        :param db_file_path: file path to the database.
        :param skip_predicates: a list of predicates, which makes all the
        statements with one of these predicates to be ignored.
        """
        super(AutoLoadableSQLiteKG, self).__init__('file:%s' % db_file_path,
                                                   **kwargs)
        self._db_file_path = db_file_path
        self._force_create_database(data, skip_predicates)
        self._kwargs = kwargs

    def _force_create_database(self, data: Iterable[Triple],
                               skip_predicates: Iterable[str]) -> None:
        # remove an already existing db
        if exists(self._db_file_path):
            remove(self._db_file_path)
        # connect and import
        self._con = connect(self._db_uri, uri=True)
        skip_predicates = set(skip_predicates) \
            if skip_predicates is not None else set([])
        logging.info('Importing statements into SQLite KG with {'
                     'skip_predicates: %s}, stored at the file "%s"'
                     % ([x for x in skip_predicates], self._db_uri))
        with _Importer(self._con, skip_predicates=skip_predicates) as importer:
            importer.import_kg(data)
        logging.info('Imported KG with {entities:%d, predicates:%d, '
                     'statements: %d}', self.entity_count,
                     self.predicate_count,
                     self.statement_count)

    def __enter__(self):
        return SQLiteKG(self._db_uri, **self._kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._con is not None:
            self._con.close()
        if exists(self._db_file_path):
            remove(self._db_file_path)
