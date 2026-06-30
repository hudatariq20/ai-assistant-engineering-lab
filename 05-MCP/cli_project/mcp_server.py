from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_documents",
    description="Read the contents of the document and return it as a string"
)
def read_documents(doc_id:str=Field(description="The id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]

@mcp.tool(
    name="edit_doc_documents",
    description="Edit a document by replacing a string in the documents with a new string"  
)
def edit_documents(
    doc_id:str=Field(description="The id of the document to edit"), 
    old_string:str=Field(description="The string to replace"), 
    new_string:str=Field(description="The new string to replace the old string with")
    ):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_string, new_string)
    return docs[doc_id]


@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_docs() -> list[str]:
    return list(docs.keys())


@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id:str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrites the contents of a document in Markdown Format"
)
def format_doc(doc_id:str = Field(description="Id of the document to format")) -> list[base.Message]:
    prompt= f"""
    Your goal is reformat a document to be written with markdown syntax.

    The id of the document you need to format is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables etc as necessary. Feel free to add in extra formatting.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted.
    """
   
    return [base.UserMessage(prompt)]
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
