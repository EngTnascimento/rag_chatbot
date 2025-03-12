from libs.common.workflows.rag.rag_state import RAGState
from libs.common.llm_providers.openai.services.openai_service import OpenaiService
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage


def generate_node(state: RAGState):
    print("---GENERATE NODE---")
    llm_service = OpenaiService()
    llm: Runnable = llm_service.chat_model

    if state["prompt_template"] is None or state["prompt_template"] == "":
        raise ValueError("Prompt template is not set")

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", state["prompt_template"]),
            MessagesPlaceholder(variable_name="messages"),
            ("user", "{question}"),
        ]
    )

    chain = prompt_template | llm | StrOutputParser()

    question = state["messages"][-1].content
    context = "\n".join([doc.page_content for doc in state["documents"]])

    print(
        f"###############################\n{state['messages']}\n###############################"
    )
    print(f"Question: {question}")

    answer = chain.invoke(
        {"question": question, "context": context, "messages": state["messages"]}
    )

    return {"messages": [AIMessage(content=answer)]}
