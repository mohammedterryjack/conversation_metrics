from typing import List

from conversation_metrics.annotators.semantics import SemanticEncoder
from conversation_metrics.metrics.utils import weighted_average
from conversation_metrics.structures.settings import ConversationSettings
from numpy.random import seed, uniform
from scipy.spatial.distance import cosine


class Entity:
    def __init__(self, text: str, thread_depth: int) -> None:
        self.text = text
        self.depth = thread_depth
        self.semantics = SemanticEncoder().vectorise(text)
        self.x = self._x_coordinate()
        self.y = self._y_coordinate()
        self._children: List["Entity"] = list()
        self._parent_similarity: float = (
            ConversationSettings.IMPOSSIBLE_ENTITY_SIMILARITY.value
        )

    def __repr__(self) -> str:
        representation = ConversationSettings.ENTITY_REPRESENTATION.value.format(
            indentation=self.depth * ConversationSettings.INDENTATION.value,
            entity_text=self.text,
            link_weight=ConversationSettings.SCORE_PLACEHOLDER.value
            if self.is_root()
            else round(self._parent_similarity, ConversationSettings.ROUND_TO.value),
        )
        for child in self._children:
            representation += f"\n{child}"
        return representation

    def __sub__(self, other: "Entity") -> float:
        """
        the semantic distance of this entity
        to some other entity (based on cosine)
        """
        return cosine(self.semantics, other.semantics)

    def is_thread_head(self) -> bool:
        """
        an entity is the head of a thread
        if it is a root (i.e. newly introduced)
        and linked to children (i.e. forms a thread)
        """
        return self.is_root() and self.is_linked()

    def is_stub(self) -> bool:
        """
        an entity is a stub (i.e. isolated)
        if it is a root (i.e. newly introduced)
        but not linked to any children (to form a thread)
        """
        return self.is_root() and not self.is_linked()

    def is_root(self) -> bool:
        """
        assumption: entities which have a negative value
        for their parent similarity are root entities
        since this is the default value and entity
        similarities will always be a positive value or 0.
        """
        return (
            self._parent_similarity
            == ConversationSettings.IMPOSSIBLE_ENTITY_SIMILARITY.value
        )

    def is_linked(self) -> bool:
        """
        if an entity has children,
        it forms a thread
        """
        return any(self._children)

    def link(self, others: List["Entity"], similarity_threshold: float) -> None:
        """
        links similar entities from list (i.e. entities within the link_radius)
        if similarity_threshold = 1.0: only identical entities link
        if similarity_threshold = 0.0: any two entities will be linked
        """
        for child, distance in zip(others, map(self.__sub__, others)):
            semantic_similarity = 1 / (1 + distance)
            if semantic_similarity >= similarity_threshold:
                child._parent_similarity = semantic_similarity
                self._children.append(child)

    def _y_coordinate(self) -> float:
        """
        the y-coordinate is based on the depth of the thread
            (negated to allow entities to flow downward)
        """
        return -float(self.depth)

    def _x_coordinate(self) -> float:
        """
        the x-coordinate is based on the semantics of the entity
            (entity's semantic vector
            is dimensionally reduced
            using a random projection
            resetting the random seed
            ensures the same random projection
            is used across entities)
        """
        seed(ConversationSettings.RANDOM_PROJECTION_SEED.value)
        random_projection = uniform(
            high=ConversationSettings.MAX_PROJECTION_WEIGHT.value,
            low=ConversationSettings.MIN_PROJECTION_WEIGHT.value,
            size=len(self.semantics),
        )
        return weighted_average(values=self.semantics, weights=random_projection)
