from libs.common.workflows.rag.rag_state import RAGState
from libs.common.workflows.rag.prompts.pandas_query_template import (
    PANDAS_QUERY_TEMPLATE,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from libs.common.llm_providers.openai.services.openai_service import OpenaiService
import pandas as pd
import numpy as np
from langchain_experimental.tools import PythonAstREPLTool


def pandas_generator_node(state: RAGState) -> RAGState:
    print("---PANDAS GENERATOR NODE---")

    df = pd.read_excel("data/excel/relatorios_gerenciais/hortifruti.xlsx")

    llm_service = OpenaiService()
    llm = llm_service.chat_model

    prompt = ChatPromptTemplate.from_template(PANDAS_QUERY_TEMPLATE)
    chain = prompt | llm | StrOutputParser()

    columns = df.columns.tolist()
    question = state["messages"][-1].content

    print(f"Columns: {columns}")

    query = chain.invoke(
        {
            "columns": columns,
            "question": question,
        }
    )

    print(f"Pandas Query: {query}")

    tool = PythonAstREPLTool(locals={"df": df})
    query_result = tool.invoke(query)

    print(f"Query result type: {type(query_result)}")
    print(f"Query Result: {query_result}")

    query_result = str(query_result)

    return {"query": query, "query_result": query_result}
