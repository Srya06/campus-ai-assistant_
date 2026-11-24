from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_chat_response(
        self,
        prompt: str,
        system_instruction: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        """Generate response given a user prompt and grounded system context."""
        pass

    @abstractmethod
    def generate_document(
        self,
        doc_type: str,
        context: str,
        tone: str,
        length: str
    ) -> Optional[str]:
        """Generate formal academic letter or email."""
        pass
