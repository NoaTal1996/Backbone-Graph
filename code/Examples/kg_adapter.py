from abc import ABC, abstractmethod
from agents.indexer_agent import IndexerAgent

class KGAdapter(ABC):
    
    @abstractmethod
    def __init__(self):
        """
        Initialize the knowledge graph adapter.
        """
        pass

    @abstractmethod
    async def get_labels(self, node: dict, category: str, agent: IndexerAgent) -> list[str]:
        """
        Get the category of the node based on its type.
        """
        pass

    @abstractmethod
    def create_node(self, node: dict, labels: list[str]) -> dict:
        """
        Create a node in the knowledge graph.
        """
        pass

    @abstractmethod
    def create_link(self, src_node_id, dst_node_id, link_type) -> dict:
        """
        Create a link between two nodes in the knowledge graph.
        """
        pass

    @abstractmethod
    def get_nodes(self) -> dict:
        """
        get all the nodes_id from the KG
        """
        pass

    @abstractmethod
    def get_links(self):
        """
        get all the link_id from the KG
        """
        pass

    @abstractmethod
    def delete_link(self, link_id: str):
        """
        removes a link from a KG
        """
        pass

    @abstractmethod
    def delete_node(self, node_id):
        """
        deletes a link from the KG
        """
        pass

    @abstractmethod
    def get_device_type_to_template_id(self, device_type: str, prompt: str, agent: IndexerAgent):
        """
        gets a device_type( e.g. router) and return a template_id (4f7eaa3f-6a36-49ca-8c5d-e39029a901a3)
        """
        pass

    @abstractmethod
    def update_status(self, node_id: str, status: str):
        """
        updates a status of a node in the KG
        """
        pass

    @abstractmethod
    def update_name(self, node_id: str, name: str):
        """
        updates a name of a node in the KG
        """
        pass

    @abstractmethod
    def query(self, cypher_query: str, paramteres: dict = None):
        """
        performs a qauery in the KG
        """
        pass

    @abstractmethod
    def get_schema(self):
        """
        recieves the schema of the kg
        """
        pass

    @abstractmethod
    def create_new_db(self, db_name: str):
        """
        duplicates the current db to a new db with the name db_name
        """
        pass

    @abstractmethod
    def delete_db(self):
        """
        deletes the current db
        """
        pass

    @abstractmethod
    def create_connection_with_retry(self):
        """
        reconnects to the KG
        """
        pass
