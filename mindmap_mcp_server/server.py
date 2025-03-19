"""
MCP Server for converting Markdown to mindmaps.
"""

import asyncio
import tempfile
import os
import shutil
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mindmap-server")

async def create_temp_file(content: str, extension: str) -> str:
    """Create a temporary file with the given content and extension."""
    temp_dir = tempfile.mkdtemp(prefix='mindmap-')
    file_path = os.path.join(temp_dir, f"input{extension}")
    
    with open(file_path, mode='w') as f:
        f.write(content)
    
    return file_path

async def run_mindmap(input_file: str, output_file: str = None, offline: bool = False, no_toolbar: bool = False) -> str:
    """Run maindmap markmap-cli on the input file and return the path to the output file."""
    args = ['npx', '-y', 'markmap-cli', input_file, '--no-open']
    
    if output_file:
        args.extend(['-o', output_file])
    else:
        output_file = os.path.splitext(input_file)[0] + '.html'
    
    if offline:
        args.append('--offline')
    
    if no_toolbar:
        args.append('--no-toolbar')
    
    try:
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            raise RuntimeError(f"markmap-cli exited with code {process.returncode}: {error_msg}")
        
        return output_file
    except Exception as e:
        raise RuntimeError(f"Failed to run markmap-cli: {str(e)}")

async def get_html_content(file_path: str) -> str:
    """Read the HTML content from the given file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

@mcp.tool()
async def convert_markdown_to_mindmap(
    markdown_content: str,  # The Markdown content to convert
    return_type: str,       # Whether to return 'html' content or 'filePath'
    offline: bool = False,  # Generate offline-capable HTML with all assets inlined
    no_toolbar: bool = False  # Hide the toolbar in the generated mindmap
) -> str:
    """Convert Markdown content to a mindmap mind map.
    
    Args:
        markdown_content: The Markdown content to convert
        return_type: Either 'html' to return the HTML content, or 'filePath' to return the file path
        offline: Whether to generate offline-capable HTML with all assets inlined
        no_toolbar: Whether to hide the toolbar in the generated mindmap
    
    Returns:
        Either the HTML content or the file path to the generated HTML
    """
    try:
        # Create a temporary markdown file
        input_file = await create_temp_file(markdown_content, '.md')
        
        # Run mindmap on it
        output_file = await run_mindmap(input_file, offline=offline, no_toolbar=no_toolbar)
        
        # Check if the output file exists
        if not os.path.exists(output_file):
            raise RuntimeError(f"Output file was not created: {output_file}")
        
        # Return either the HTML content or the file path
        if return_type == 'html':
            html_content = await get_html_content(output_file)
            return html_content
        else:
            return output_file
    except Exception as e:
        raise RuntimeError(f"Error converting Markdown to mindmap: {str(e)}")

def main():
    """Entry point for the mindmap-mcp-server command."""
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
