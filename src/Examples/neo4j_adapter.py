from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
import time

from tools.kg_adapter import KGAdapter

# Langchain Graph for update_schema
from langchain_community.graphs import Neo4jGraph

# Indexer Agent
from agents.indexer_agent import IndexerAgent

# labels memory
import os
import pickle

class Neo4jAdapter(KGAdapter):
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str, neo4j_db: str, create_db = False):
        super().__init__()
        self._neo4j_uri = neo4j_uri
        self._neo4j_user = neo4j_user
        self._neo4j_password = neo4j_password
        self._neo4j_db = neo4j_db
        self._create_db = create_db

    def init_db(self):
        if self._create_db:
            self.create_new_db(self._neo4j_db)

        self.create_connection_with_retry()
        self.langchain_neo4j = Neo4jGraph(
            url=self._neo4j_uri,
            username=self._neo4j_user,
            password=self._neo4j_password,
            database=self._neo4j_db
        )

    def create_node(self, node: dict, labels: list[str]):
        """recives as input a node and inserts him into neo4j"""
        with self.neo4j_driver.session() as session:
            properties = {
                'node_id': node['node_id'],
                'name': node['name'],
                'node_type': node['node_type'],
                'status': node['status'],
                'console': node['console'] if node['console'] is not None else 'None',
                'console_type': node['console_type'],
                'mac_address': node['properties'].get('mac_address', None),
            }

            # Construct the query properly
            query = f"""
            CREATE (node:{':'.join(labels)} {{
                node_id: $node_id,
                name: $name,
                node_type: $node_type,
                status: $status,
                console: $console,
                console_type: $console_type
            }})
            """

            session.execute_write(lambda tx: tx.run(query, **properties))

    def create_link(self, link: dict):
        """Receives a link and creates a relationship between two nodes in Neo4j"""
        with self.neo4j_driver.session() as session:
            link_id = link['link_id']
            link_type = link['link_type']

            # Extract the source and target node information
            if len(link['nodes']) >= 2:
                source_node = link['nodes'][0]
                target_node = link['nodes'][1]

                # Extract interface names from labels
                source_interface = source_node['label']['text'] if 'label' in source_node and 'text' in source_node['label'] else ""
                target_interface = target_node['label']['text'] if 'label' in target_node and 'text' in target_node['label'] else ""

                # Create the relationship with all relevant properties
                query = """
                MATCH (source), (target)
                WHERE source.node_id = $source_id AND target.node_id = $target_id
                CREATE (source)-[r:CONNECTED_TO {
                    link_id: $link_id,
                    link_type: $link_type,
                    source_adapter: $source_adapter,
                    source_port: $source_port,
                    source_interface: $source_interface,
                    target_adapter: $target_adapter,
                    target_port: $target_port,
                    target_interface: $target_interface
                }]->(target)
                """

                session.execute_write(lambda tx: tx.run(query,
                                                        link_id=link_id,
                                                        link_type=link_type,
                                                        source_id=source_node['node_id'],
                                                        source_adapter=source_node['adapter_number'],
                                                        source_port=source_node['port_number'],
                                                        source_interface=source_interface,
                                                        target_id=target_node['node_id'],
                                                        target_adapter=target_node['adapter_number'],
                                                        target_port=target_node['port_number'],
                                                        target_interface=target_interface
                                                        ))

    def get_nodes(self):
        with self.neo4j_driver.session() as session:
            result = session.execute_read(
                lambda tx: tx.run("MATCH (n) RETURN n").values())
            return [record[0] for record in result]

    def get_links(self):
        with self.neo4j_driver.session() as session:
            result = session.execute_read(lambda tx: tx.run(
                "MATCH ()-[r:CONNECTED_TO]->() RETURN r.link_id AS link_id").values())
            return [record[0] for record in result]


    def create_connection_with_retry(self, max_retries=5):
        try:
            if not hasattr(self, 'neo4j_driver'):
                raise Exception("Driver not initialized")
            self.neo4j_driver.verify_connectivity()
        except Exception as e:
            if hasattr(self, 'neo4j_driver'):
                self.neo4j_driver.close()
            for attempt in range(max_retries):
                try:
                    driver = GraphDatabase.driver(self._neo4j_uri, auth=(self._neo4j_user, self._neo4j_password), database=self._neo4j_db)
                    driver.verify_connectivity()
                    self.neo4j_driver = driver
                    return
                except Exception as e:
                    print(f"Connection attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise
    
    def query(self, cypher_query: str, paramteres: dict = None):
        with self.neo4j_driver.session() as session:
            return list(session.run(cypher_query, paramteres or {}))
    
    def get_schema(self):
        with self.neo4j_driver.session() as session:
            result = session.run("CALL db.schema.visualization()")
            schema = result.single()
        return schema

    async def get_labels(self, node: dict, category: str, agent: IndexerAgent):
        """
        Get the category of the node based on its type.
        The labels are used to search the node in the knowledge graph.
        """
        async def ask(node_type, template_id):
            return await agent.run(task=f"get labels for {node_type} {template_id}")
        
        node_type = node["node_type"]
        template_id = node["template_id"]

        if category != "guest":
            return [category] if category == node_type else [category, node_type]

        if node_type == "cloud":
            return ["cloud"]

        if node_type == "vpcs":
            return ["vpcs", "PC", category]

        # Try loading classification from memory
        memory_path = os.path.abspath("data/memory/labels_classification_memory.pkl")
        try:
            if os.path.getsize(memory_path) == 0:
                raise EOFError("Memory file is empty.")
            with open(memory_path, "rb") as f:
                memory = pickle.load(f)
                memory_result = memory.get(template_id)
                if memory_result:
                    return memory_result
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            pass  # Memory will be recomputed below

        # Memory miss: classify using the agent
        result = await ask(node_type, template_id)
        labels = [label.strip() for label in result.messages[-1].content.split(",")]

        # Save to memory and file
        agent.add_classifcation(template_id, labels)
        print(f"classified {node_type} {template_id} as {labels}")

        # Append category for docker or guest
        if node_type == "docker":
            return ["docker", *labels, category]
        return [*labels, category]
    
    async def get_device_type_to_template_id(self, device_type: str, prompt: str, agent: IndexerAgent):
        if device_type == "firewall":
            return "4f7eaa3f-6a36-49ca-8c5d-e39029a901a3"
        elif device_type == "router":
            return "c760404f-33f2-4672-9245-e4a185b78213"
        elif device_type == "switch":
            return "59d74309-f339-4d02-a2f5-286550d318b7"
        else:
            return None


    def delete_link(self, link_id: str):
        """
        deletes a link with link_id
        """
        with self.neo4j_driver.session() as session:
            session.execute_write(lambda tx: tx.run(
                "MATCH ()-[r:CONNECTED_TO {link_id: $link_id}]->() DELETE r", link_id=link_id))
            
    def delete_node(self, node_id: str):
        """
        deletes a node from a KG
        """
        with self.neo4j_driver.session() as session:
            session.execute_write(lambda tx: tx.run(
                "MATCH (n {node_id: $node_id}) DETACH DELETE n", node_id=node_id))

    def update_status(self, node_id: str, status: str):
        """
        updates a status of a node in the KG
        """
        with self.neo4j_driver.session() as session:
            session.execute_write(lambda tx: tx.run(
                "MATCH (n {node_id: $node_id}) SET n.status = $status", 
                node_id=node_id, status=status))
    
    def update_name(self, node_id, name):
        with self.neo4j_driver.session() as session:
            session.execute_write(lambda tx: tx.run(
                "MATCH (n {node_id: $node_id}) SET n.name = $name", 
                node_id=node_id, name=name))
            
    def get_schema(self):
        """
        returns the schema of the KG
        """
        self.langchain_neo4j.refresh_schema()
        return self.langchain_neo4j.schema

    def create_new_db(self, db_name: str):
        try:
            driver = GraphDatabase.driver(self._neo4j_uri, auth=(self._neo4j_user, self._neo4j_password))
            with driver.session(database="system") as session:
                session.run(f"CREATE DATABASE `{db_name}` IF NOT EXISTS")

            for _ in range(10):
                try:
                    with driver.session(database=db_name) as session:
                        session.run("RETURN 1")
                    break  
                except ClientError:
                    time.sleep(1)
            else:
                raise Exception(f"Database {db_name} not available after creation")
        except Exception as e:
            raise Exception(f"Failed to duplicate database: {e}")
        finally:
            driver.close()

    def delete_db(self):
        """
        Deletes a database in Neo4j.
        """
        try:
            with self.neo4j_driver.session(database="system") as session:
                session.run(f"DROP DATABASE `{self._neo4j_db}` IF EXISTS")
        finally:
            self.neo4j_driver.close()