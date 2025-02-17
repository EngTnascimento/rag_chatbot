from abc import ABC, abstractmethod
from typing import Any


class WorkflowTrait(ABC):
    """Abstract base class defining the interface for workflows."""

    @abstractmethod
    async def execute(self, state) -> Any:
        """
        Execute the workflow with the given input.

        Args:
            input (Any): The input to process through the workflow

        Returns:
            Any: The result of the workflow execution
        """
        pass
