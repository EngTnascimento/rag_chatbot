from libs.common.llm_providers.openai.services.openai_service import OpenaiService
from libs.common.workflows.rag.rag_workflow import RAGWorkflow
import logging
from chat.prompt_templates import RAG_TEMPLATE

logger = logging.getLogger(__name__)


class RAGAgent:
    def __init__(self, llm_service: OpenaiService = OpenaiService()):
        self.llm_service = llm_service
        self.workflow = RAGWorkflow(self.llm_service)

    async def chat(self, user_message: str, user_id: str) -> str:
        answer = await self.workflow.execute(user_message, user_id, RAG_TEMPLATE)
        return answer
