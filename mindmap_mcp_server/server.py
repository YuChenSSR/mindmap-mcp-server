"""
MCP Server for converting Markdown to mindmaps.
"""

import asyncio
import tempfile
import os
import shutil
import sys
import argparse
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='MCP Server for converting Markdown to mindmaps')
    parser.add_argument('--return-type', choices=['html', 'filePath'], default='html',
                        help='Whether to return HTML content or file path. Default: html')
    return parser.parse_args()

# Global configuration
args = parse_arguments()
RETURN_TYPE = args.return_type

# Initialize FastMCP server
mcp = FastMCP("mindmap-server")

async def create_temp_file(content: str, extension: str) -> str:
    """Create a temporary file with the given content and extension."""
    temp_dir = tempfile.mkdtemp(prefix='mindmap-')
    file_path = os.path.join(temp_dir, f"input{extension}")
    
    with open(file_path, mode='w') as f:
        f.write(content)
    
    return file_path

async def run_mindmap(input_file: str, output_file: str = None) -> str:
    """Run markmap-cli on the input file and return the path to the output file."""
    args = ['npx', '-y', 'markmap-cli', input_file, '--no-open']
    
    if output_file:
        args.extend(['-o', output_file])
    else:
        output_file = os.path.splitext(input_file)[0] + '.html'
    
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
) -> str:
    """Convert Markdown content to a mindmap mind map.
    
    Args:
        markdown_content: The Markdown content to convert
    
    Returns:
        Either the HTML content or the file path to the generated HTML, 
        depending on the --return-type server argument
    """
    try:
        # Create a temporary markdown file
        input_file = await create_temp_file(markdown_content, '.md')
        
        # Run mindmap on it
        output_file = await run_mindmap(input_file)
        
        # Check if the output file exists
        if not os.path.exists(output_file):
            raise RuntimeError(f"Output file was not created: {output_file}")
        
        # Return either the HTML content or the file path based on command line arg
        if RETURN_TYPE == 'html':
            html_content = await get_html_content(output_file)
            return html_content
        else:
            return output_file
    except Exception as e:
        raise RuntimeError(f"Error converting Markdown to mindmap: {str(e)}")

def main():
    """Entry point for the mindmap-mcp-server command."""
    global args, RETURN_TYPE
    
    # Parse arguments again to ensure parameters are captured when running as an entry point
    args = parse_arguments()
    RETURN_TYPE = args.return_type
    
    print(f"Starting mindmap-mcp-server with return type: {RETURN_TYPE}", file=sys.stderr)
    
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()