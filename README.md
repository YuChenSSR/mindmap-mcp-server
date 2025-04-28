# Mindmap MCP Server

<p align="center">
  <img src="https://raw.githubusercontent.com/YuChenSSR/pics/master/imgs/2025-03-21/JMi7Mn89Hw5ikd9z.jpeg" alt="mindmap_mcp" width="50%">
</p>

A Model Context Protocol (MCP) server for converting Markdown content to interactive mindmaps.



## Installation

```bash
pip install mindmap-mcp-server
```

Or using `uvx`:

```bash
uvx mindmap-mcp-server
```
Or using `docker` safer and easier.

## Attention

Three installation methods have been successfully tested on macOS and Linux. 

For Windows users experiencing issues with `npx` for this MCP, consider using the Docker method. Alternatively, if you use Visual Studio Code, the ["Markmap"](https://marketplace.visualstudio.com/items?itemName=gera2ld.markmap-vscode) extension offers a potentially simpler solution than navigating command-line tools.

## Prerequisites

This package requires Node.js to be installed when using command `python` or `uvx` to run the server.



## Usage

### With Claude Desktop or other MCP clients

Add this server to your `claude_desktop_config.json`:

<details>
 
 <summary>using `uvx`:</summary>

```json
{
  "mcpServers": {
    "mindmap": {
      "command": "uvx",
      "args": ["mindmap-mcp-server", "--return-type", "html"]
    }
  }
}
```

or  

recommended:

```json
{
  "mcpServers": {
    "mindmap": {
      "command": "uvx",
      "args": ["mindmap-mcp-server", "--return-type", "filePath"]
    }
  }
}
```

we use `--return-type` to specify the return type of the mindmap content, you can choose `html` or `filePath` according to your needs.   
`html` will return the entire HTML content of the mindmap, which you can preview in your AI client's artifact; 

![return_html_content](https://raw.githubusercontent.com/YuChenSSR/pics/master/imgs/2025-03-20/qAEimhwZJDQ3NBLs.png)

![html_preview](https://raw.githubusercontent.com/YuChenSSR/pics/master/imgs/2025-03-21/SujqY2L5lhWSHWvi.png)


`filePath` will save the mindmap to a file and return the file path,which you can open in your browser. It can **save your tokens** !

![generate_file](https://raw.githubusercontent.com/YuChenSSR/pics/master/imgs/2025-03-20/WDqlWhsoiAYpLmBF.png)

![file_to_open](https://raw.githubusercontent.com/YuChenSSR/pics/master/imgs/2025-03-20/jfRIDc5mfvNtKykC.png) 

</details>

<details>
<summary>using `python`:</summary>

Using [a specific Python file](https://github.com/YuChenSSR/mindmap-mcp-server/blob/main/mindmap_mcp_server/server.py) in this repository:


```json
{
  "mcpServers": {
    "mindmap": {
      "command": "python",
      "args": ["/path/to/your/mindmap_mcp_server/server.py", "--return-type", "html"]
    }
  }
}
```
  
or   

```json
{
  "mcpServers": {
    "mindmap": {
      "command": "python",
      "args": ["/path/to/your/mindmap_mcp_server/server.py", "--return-type", "filePath"]
    }
  }
}
```
we use `--return-type` to specify the return type of the mindmap content, you can choose `html` or `filePath` according to your needs. see using \`uvx\` for more details.

</details>

<details>

<summary>using `docker`:</summary>

First, you pull the image:

```bash
docker pull ychen94/mindmap-converter-mcp
```

Second, set the server:

```json
{
  "mcpServers": {
    "mindmap-converter": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "-v", "/path/to/output/folder:/output", "ychen94/mindmap-converter-mcp:latest"]
    }
  }
}
```
⚠️ Replace `/path/to/output/folder` with an actual path on your system where you want to save mind maps, such as `/Users/username/Downloads` on macOS or `C:\\Users\\username\\Downloads` on Windows.

**Tools Provided in the docker container**
The server provides the following MCP tools:
1. **markdown-to-mindmap-content**  
Converts Markdown to an HTML mind map and returns the entire HTML content.  
You don't use the args: `-v` and `/path/to/output/folder:/output` in the command `docker`.  
**Parameters**:   
	•	markdown (string, required): The Markdown content to convert  
	•	toolbar (boolean, optional): Whether to show the toolbar (default: true)  
**Best for**: Simple mind maps where the HTML content size isn't a concern. And you can use **artifact** in your AI client to preview the mindmap.  
2. **markdown-to-mindmap-file**  
Converts Markdown to an HTML mind map and saves it to a file in the mounted directory.  
**Parameters**:  
	•	markdown (string, required): The Markdown content to convert  
	•	filename (string, optional): Custom filename (default: auto-generated timestamp name)  
	•	toolbar (boolean, optional): Whether to show the toolbar (default: true)  
**Best for**: Complex mind maps or when you want to **save the tokens** for later use.  
you can open the html file in your browser to view the mindmap. Also you can use the [iterm-mcp-server](https://github.com/ferrislucas/iterm-mcp) or other terminals' mcp servers to open the file in your browser without interrupting your workflow.  

</details>

### Troubleshooting 

**File Not Found**  
If your mind map file isn't accessible:  
	1	Check that you've correctly mounted a volume to the Docker container  
	2	Ensure the path format is correct for your operating system  
	3	Make sure Docker has permission to access the directory  
 
**Docker Command Not Found**  
	1	Verify Docker is installed and in your PATH  
	2	Try using the absolute path to Docker  
 
**Server Not Appearing in Claude**  
	1	Restart Claude for Desktop after configuration changes  
	2	Check Claude logs for connection errors  
	3	Verify Docker is running  

**Advanced Usage  
Using with Other MCP Clients**  
This server works with any MCP-compatible client, not just Claude for Desktop. The server implements the Model Context Protocol (MCP) version 1.0 specification.  




## Features  

This server provides a tool for converting Markdown content to mindmaps using the `markmap-cli` library:  

- Convert Markdown to interactive mindmap HTML  
- Option to create offline-capable mindmaps  
- Option to hide the toolbar  
- Return either HTML content or file path  

## Example  

In Claude, you can ask:

1. 
"**give a mindmap for the following markdown code, using a mindmap tool:**
```
# Project Planning
## Research
### Market Analysis
### Competitor Review
## Design
### Wireframes
### Mockups
## Development
### Frontend
### Backend
## Testing
### Unit Tests
### User Testing
```
"


if you want to save the mindmap to a file, and then open it in your browser using the iTerm MCP server:   

2. 
"**give a mindmap for the following markdown input_code using a mindmap tool,
after that,use iterm to open the generated html file.
input_code:**
```
markdown content
```
"


3.
"**Think about the process of putting an elephant into a refrigerator, and provide a mind map. Open it with a terminal.**"

<details>
	
<summary>see the result</summary>
	
![aiworkflow](https://raw.githubusercontent.com/YuChenSSR/pics/master/imgs/2025-03-22/QUjGnpmUcPfd3lBI.png)

![mindmapinbrowser](https://raw.githubusercontent.com/YuChenSSR/pics/master/imgs/2025-03-22/w7DZ4shFhLoQZruq.png)

 </details>

 
**and more**


## License

This project is licensed under the MIT License.
For more details, please see the LICENSE file in [this project repository](https://github.com/YuChenSSR/mindmap-mcp-server)  
 
---
 
If this project is helpful to you, please consider giving it a Star ⭐️

The advancement of technology ought to benefit all individuals rather than exploit the general populace.
