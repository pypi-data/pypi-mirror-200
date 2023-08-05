"""Keyword-table based index.

Similar to a "hash table" in concept. LlamaIndex first tries
to extract keywords from the source text, and stores the
keywords as keys per item. It similarly extracts keywords
from the query text. Then, it tries to match those keywords to
existing keywords in the table.

"""

import logging
from typing import Any, Dict, List, Optional, Sequence, Tuple

from gpt_index.data_structs.data_structs_v2 import KG
from gpt_index.data_structs.node_v2 import Node
from gpt_index.indices.base import BaseGPTIndex, QueryMap
from gpt_index.indices.query.knowledge_graph.query import GPTKGTableQuery, KGQueryMode
from gpt_index.indices.query.schema import QueryMode
from gpt_index.prompts.default_prompts import (
    DEFAULT_KG_TRIPLET_EXTRACT_PROMPT,
    DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE,
)
from gpt_index.prompts.prompts import KnowledgeGraphPrompt

DQKET = DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE

logger = logging.getLogger(__name__)


class GPTKnowledgeGraphIndex(BaseGPTIndex[KG]):
    """GPT Knowledge Graph Index.

    Build a KG by extracting triplets, and leveraging the KG during query-time.

    Args:
        kg_triple_extract_template (KnowledgeGraphPrompt): The prompt to use for
            extracting triplets.
        max_triplets_per_chunk (int): The maximum number of triplets to extract.

    """

    index_struct_cls = KG

    def __init__(
        self,
        nodes: Optional[Sequence[Node]] = None,
        index_struct: Optional[KG] = None,
        kg_triple_extract_template: Optional[KnowledgeGraphPrompt] = None,
        max_triplets_per_chunk: int = 10,
        include_embeddings: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        # need to set parameters before building index in base class.
        self.include_embeddings = include_embeddings
        self.max_triplets_per_chunk = max_triplets_per_chunk
        self.kg_triple_extract_template = (
            kg_triple_extract_template or DEFAULT_KG_TRIPLET_EXTRACT_PROMPT
        )
        # NOTE: Partially format keyword extract template here.
        self.kg_triple_extract_template = (
            self.kg_triple_extract_template.partial_format(
                max_knowledge_triplets=self.max_triplets_per_chunk
            )
        )
        super().__init__(
            nodes=nodes,
            index_struct=index_struct,
            **kwargs,
        )

    @classmethod
    def get_query_map(self) -> QueryMap:
        """Get query map."""
        return {
            QueryMode.DEFAULT: GPTKGTableQuery,
        }

    def _extract_triplets(self, text: str) -> List[Tuple[str, str, str]]:
        """Extract keywords from text."""
        response, _ = self._service_context.llm_predictor.predict(
            self.kg_triple_extract_template,
            text=text,
        )
        return self._parse_triplet_response(response)

    @staticmethod
    def _parse_triplet_response(response: str) -> List[Tuple[str, str, str]]:
        knowledge_strs = response.strip().split("\n")
        results = []
        for text in knowledge_strs:
            tokens = text[1:-1].split(",")
            if len(tokens) != 3:
                continue
            subj, pred, obj = tokens
            results.append((subj.strip(), pred.strip(), obj.strip()))
        return results

    def _build_index_from_nodes(self, nodes: Sequence[Node]) -> KG:
        """Build the index from nodes."""
        # do simple concatenation
        index_struct = KG(table={})
        for n in nodes:
            triplets = self._extract_triplets(n.get_text())
            logger.debug(f"> Extracted triplets: {triplets}")
            for triplet in triplets:
                index_struct.upsert_triplet(triplet, n)

            if self.include_embeddings:
                for i, triplet in enumerate(triplets):
                    self._service_context.embed_model.queue_text_for_embeddding(
                        str(triplet), str(triplet)
                    )

                embed_outputs = (
                    self._service_context.embed_model.get_queued_text_embeddings()
                )
                for rel_text, rel_embed in zip(*embed_outputs):
                    index_struct.add_to_embedding_dict(rel_text, rel_embed)

        return index_struct

    def _insert(self, nodes: Sequence[Node], **insert_kwargs: Any) -> None:
        """Insert a document."""
        for n in nodes:
            triplets = self._extract_triplets(n.get_text())
            logger.debug(f"Extracted triplets: {triplets}")
            for triplet in triplets:
                triplet_str = str(triplet)
                self._index_struct.upsert_triplet(triplet, n)
                if (
                    self.include_embeddings
                    and triplet_str not in self._index_struct.embedding_dict
                ):
                    rel_embedding = (
                        self._service_context.embed_model.get_text_embedding(
                            triplet_str
                        )
                    )
                    self.index_struct.add_to_embedding_dict(triplet_str, rel_embedding)

    def _delete(self, doc_id: str, **delete_kwargs: Any) -> None:
        """Delete a document."""
        raise NotImplementedError("Delete is not supported for KG index yet.")

    def _preprocess_query(self, mode: QueryMode, query_kwargs: Dict) -> None:
        """Set the default embedding mode during query based on current index."""
        if (
            len(self.index_struct.embedding_dict) > 0
            and "embedding_mode" not in query_kwargs
        ):
            query_kwargs["embedding_mode"] = KGQueryMode.HYBRID

    def get_networkx_graph(self) -> Any:
        """Get networkx representation of the graph structure.

        NOTE: This function requires networkx to be installed.
        NOTE: This is a beta feature.

        """
        try:
            import networkx as nx
        except ImportError:
            raise ImportError(
                "Please install networkx to visualize the graph: `pip install networkx`"
            )

        g = nx.Graph()
        # add nodes
        for node_name in self.index_struct.table.keys():
            g.add_node(node_name)

        # add edges
        rel_map = self.index_struct.rel_map
        for keyword in rel_map.keys():
            for obj, rel in rel_map[keyword]:
                g.add_edge(keyword, obj, title=rel)

        return g
