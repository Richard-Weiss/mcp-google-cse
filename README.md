# Google Custom Search Engine MCP Server

A Model Context Protocol server that provides search capabilities using a CSE (custom search engine). This server enables LLMs to provide a regular google search term and returns the found search results.

The tool only returns the results itself and not the content, the tool should be combined with other servers like [mcp-server-fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) to extract the content from the search results.
You may also combine it with other tools to enable some kind of "deep search" or tool chaining in general.

**The free quota is 100 searches (1 tool call == 1 search) per day, if you don't want to set up billing and this is insufficient for your use case, you should consider using another server.**

<a href="https://glama.ai/mcp/servers/mieczol4lv"><img width="380" height="200" src="https://glama.ai/mcp/servers/mieczol4lv/badge" alt="Google Custom Search Engine Server MCP server" /></a>
[![smithery badge](https://smithery.ai/badge/@Richard-Weiss/mcp-google-cse)](https://smithery.ai/server/@Richard-Weiss/mcp-google-cse)

## Available Tools

- `google_search` - Searches the custom search engine using the search term and returns a list of results containing the title, link and snippet of each result.
    - `search_term` (string, required): The search term to search for, equaling the [query parameter](https://bit.ly/AllTheOperators) `q` in the usual Google search.

## Environment variables

- `API_KEY` (required): The API key for the custom search engine.
- `ENGINE_ID` (required): The engine ID for the custom search engine.
- `SERVICE_NAME` (required/optional): The name of the service, leave empty if you haven't changed the name (customsearch).
- `COUNTRY_REGION` (optional): Restricts search results to documents originating in a particular country. See [Country Parameter Values](https://developers.google.com/custom-search/docs/json_api_reference#countryCollections) for valid values.
- `GEOLOCATION` (optional, default "us"): The geolocation of the end-user performing the search. See [Geolocation Parameter Values](https://developers.google.com/custom-search/docs/json_api_reference#countryCodes) for valid values.
- `RESULT_LANGUAGE` (optional, default "lang_en"): The language of the search results. See [CSE Query parameters, lr](https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list?apix=true#query-parameters) for valid values.
- `RESULT_NUM` (optional, default 10): The number of search results to return. Range from 1-10.

## CSE Setup
Creating a custom search engine is comparatively easy, completely free and can be done in under 5 minutes.

1. Go to https://console.cloud.google.com/ and create a new project. Call it "Claude CSE" for example.
2. Select the project and search for "Custom Search API" in the search bar.
3. Click on the search result and click on "Enable".
4. Click on the Credentials tab and create a new API key.
5. Go to https://programmablesearchengine.google.com to create a new custom search engine.
6. Create a new search engine and give it any name, the name doesn't correlate to SERVICE_NAME.
7. Select "Search the entire web" if you want a normal Google Search experience.
8. Click on "Create" and copy the engine id from the js code, or hit customize and get it from the overview.
9. You can optionally customize the search engine to your liking.

With the default quota, you will get 100 searches per day for free. A tool call only costs 1 search, even if you get 10 results for example.


## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-google-cse*.

### Using PIP

Alternatively you can install `mcp-google-cse` via pip:

```
pip install mcp-google-cse
```

After installation, you can run it as a script using:

```
python -m mcp-google-cse
```

### Installing via Smithery

To install Google Custom Search Engine for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@Richard-Weiss/mcp-google-cse):

```bash
npx -y @smithery/cli install @Richard-Weiss/mcp-google-cse --client claude
```

## Configuration

### Configure for Claude app

Add to your `claude_desktop_config.json`:


#### Using uvx (use this if you don't know which one to choose)
```
"mcp-google-cse": {
    "command": "uvx",
    "args": ["mcp-google-cse"],
    "env": {
        "API_KEY": "",
        "ENGINE_ID": ""
    }
}
```


#### Using pip installation

```
"mcp-google-cse": {
    "command": "python",
    "args": ["-m", "mcp-google-cse"],
    "env": {
        "API_KEY": "",
        "ENGINE_ID": ""
    }
}
```

#### Running locally

```
    "mcp-google-cse": {
      "command": "uv",
      "args": [
        "--directory",
        "{{Path to the cloned repo",
        "run",
        "mcp-google-cse"
      ],
      "env": {
        "API_KEY": "",
        "ENGINE_ID": ""
      }
    }
```

### Example result
google_search("What is MCP after:2024-11-01")
Result:
```json
[
    {
        "title": "Can someone explain MCP to me? How are you using it? And what ...",
        "link": "https://www.reddit.com/r/ClaudeAI/comments/1h55zxd/can_someone_explain_mcp_to_me_how_are_you_using/",
        "snippet": "Dec 2, 2024 ... Comments Section ... MCP essentially allows you to give Claude access to various external systems. This can be files on your computer, an API, a browser, a ..."
    },
    {
        "title": "Introducing the Model Context Protocol \\ Anthropic",
        "link": "https://www.anthropic.com/news/model-context-protocol",
        "snippet": "Nov 25, 2024 ... The Model Context Protocol (MCP) is an open standard for connecting AI assistants to the systems where data lives, including content repositories, ..."
    },
    {
        "title": "3.5 Sonnet + MCP + Aider = Complete Game Changer : r ...",
        "link": "https://www.reddit.com/r/ChatGPTCoding/comments/1hwn6qd/35_sonnet_mcp_aider_complete_game_changer/",
        "snippet": "Jan 8, 2025 ... Really cool stuff. For those out of the loop here are some MCP servers. You can give your Claude chat (in the desktop version, or in a tool like Cline) ..."
    },
    {
        "title": "Announcing Spring AI MCP: A Java SDK for the Model Context ...",
        "link": "https://spring.io/blog/2024/12/11/spring-ai-mcp-announcement",
        "snippet": "Dec 11, 2024 ... This SDK will enable Java developers to easily connect with an expanding array of AI models and tools while maintaining consistent, reliable integration ..."
    },
    {
        "title": "Implementing a MCP server in Quarkus - Quarkus",
        "link": "https://quarkus.io/blog/mcp-server/",
        "snippet": "6 days ago ... The Model Context Protocol (MCP) is an emerging standard that enables AI models to safely interact with external tools and resources. In this tutorial, I'll ..."
    },
    {
        "title": "mark3labs/mcp-go: A Go implementation of the Model ... - GitHub",
        "link": "https://github.com/mark3labs/mcp-go",
        "snippet": "Dec 18, 2024 ... A Go implementation of the Model Context Protocol (MCP), enabling seamless integration between LLM applications and external data sources and tools."
    },
    {
        "title": "MCP enables Claude to Build, Run and Test Web Apps by Looking ...",
        "link": "https://wonderwhy-er.medium.com/mcp-enable-claude-to-build-run-and-test-web-apps-using-screenshots-3ae06aea6c4a",
        "snippet": "Dec 18, 2024 ... How to Replicate My Experiment on Your Machine. If you're ready to dive into setting up MCP for Claude, follow these steps: ... 2. Download the Project: ... 3."
    },
    {
        "title": "MCP definition and meaning | Collins English Dictionary",
        "link": "https://www.collinsdictionary.com/dictionary/english/mcp",
        "snippet": "2 days ago ... 2 meanings: male chauvinist pig → informal, derogatory a man who exhibits male chauvinism Abbreviation: MCP.... Click for more definitions."
    },
    {
        "title": "What is Anthropic's New MCP Standard and How Can It Improve ...",
        "link": "https://dappier.medium.com/what-is-anthropics-new-mcp-standard-and-how-can-it-improve-your-ai-agent-be6f6c72eb6a",
        "snippet": "Nov 26, 2024 ... Anthropic has released a new protocol, MCP, for connecting AI agents to data sets. This blog explores when and why developers might use MCP to improve their ..."
    },
    {
        "title": "Mostafa Gharib on LinkedIn: What is MCP and how it works",
        "link": "https://www.linkedin.com/posts/mostafa-gharib_what-is-mcp-and-how-it-works-activity-7274301560594026497-p_yq",
        "snippet": "Dec 15, 2024 ... ... MCP Host can use. (Bonus: SDKs in Python and TypeScript make it easy to build these servers!) 2️⃣ MCP Clients These interact with MCP Servers via the protocol."
    }
]
```
