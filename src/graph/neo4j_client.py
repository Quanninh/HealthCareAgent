"""Neo4j client connection manager and Cypher query execution wrapper.
"""

import logging
from typing import Any, Dict, List, Optional

# Suppress benign GQL notifications from Neo4j server (e.g. 01G11 null eliminated in set function)
logging.getLogger("neo4j.notifications").setLevel(logging.ERROR)

try:
    from neo4j import GraphDatabase, Driver
except ImportError:
    Driver = Any
    GraphDatabase = None


class Neo4jClient:
    """Thread-safe Neo4j driver wrapper for executing Cypher transactions."""

    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        user: str = "neo4j",
        password: str = "password",
        database: str = "neo4j"
    ):
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database
        self.driver: Optional[Driver] = None

    def connect(self) -> bool:
        """Initializes driver connection and verifies connectivity."""
        if GraphDatabase is None:
            raise ImportError("The 'neo4j' package is not installed. Install via: pip install neo4j")

        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                max_connection_lifetime=3600
            )
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            print(f"[Neo4jClient] Connection failed to {self.uri}: {e}")
            return False

    def close(self):
        """Closes active driver connection."""
        if self.driver:
            self.driver.close()
            self.driver = None

    def query(self, cypher: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executes a Cypher read query and returns records as a list of dicts."""
        if not self.driver:
            raise ConnectionError("Neo4j driver is not connected. Call connect() first.")

        parameters = parameters or {}
        with self.driver.session(database=self.database) as session:
            result = session.run(cypher, parameters)
            return [record.data() for record in result]

    def execute_write(self, cypher: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Executes a Cypher write transaction."""
        if not self.driver:
            raise ConnectionError("Neo4j driver is not connected. Call connect() first.")

        parameters = parameters or {}
        with self.driver.session(database=self.database) as session:
            return session.execute_write(lambda tx: tx.run(cypher, parameters).consume())

    def apply_schema(self, constraints: List[str], indexes: List[str]):
        """Applies uniqueness constraints and indexes to the database."""
        for stmt in constraints + indexes:
            try:
                self.execute_write(stmt)
            except Exception as e:
                # Some Neo4j versions may warn if constraint already exists
                pass
