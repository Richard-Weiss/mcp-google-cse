import os
from sys import stdin, stdout
from typing import Any, List

from googleapiclient.discovery import build
from mcp import Tool, stdio_server
from mcp.server.lowlevel import Server
from mcp.types import TextContent, ImageContent, EmbeddedResource

stdin.reconfigure(encoding='utf-8')
stdout.reconfigure(encoding='utf-8')

server = Server("mcp-google-cse")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        Tool(
            name="google_search",
            description="Search the custom search engine using the search term. Regular query arguments can also be used, like appending site:reddit.com or after:2024-04-30. If available and/or requested, the links of the search results should be used in a follow-up request using a different tool to get the full content. Example: \"claude.ai features site:reddit.com after:2024-04-30\"",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {"type": "string"},
                },
                "required": ["search_term"],
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
) -> list[TextContent | ImageContent | EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    search_term = arguments.get('search_term', '')

    if name == 'google_search' and search_term != '':
        result = await google_search(search_term)
        return result
    else:
        raise ValueError(f"Unknown tool: {name}")


async def google_search(search_term: str) -> List[TextContent]:
    """
    Search the custom search engine using the search term.
    :param search_term: The search term to search for, equaling the q argument in Google's search.
    :return: Search results containing the title, link and snippet of the search result.
    """
    service = build(os.getenv('SERVICE_NAME', 'customsearch'), "v1", developerKey=os.getenv('API_KEY'))
    response = service.cse().list(
        q=search_term,
        cx=os.getenv('ENGINE_ID'),
        cr=os.getenv('COUNTRY_REGION'),
        gl=os.getenv('GEOLOCATION', 'us'),
        lr=os.getenv('RESULT_LANGUAGE', 'lang_en'),
        num=os.getenv('RESULT_NUM', 10),
        fields='items(title,link,snippet)').execute()
    results = response['items']
    __clean_up_snippets(results)

    text_contents = []

    for result in results:
        text_contents.append(
            TextContent(
                type="text",
                text=f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}"
            )
        )

    return text_contents


def __clean_up_snippets(items: List[dict]) -> None:
    """
    Remove non-breaking space and trailing whitespace from snippets.
    :param items: The search results that contain snippets that have to be cleaned up.
    :return: Nothing, the dict is mutable and updated directly.
    """
    for item in items:
        item.update({k: v.replace('\xa0', ' ').strip() if k == 'snippet' else v for k, v in item.items()})


async def run() -> None:
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            options
        )
