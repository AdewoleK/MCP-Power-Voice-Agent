from mcp.server import FastMCP
mcp = FastMCP("SupabaseAgent")

@mcp.tool()
def query_database(query: str) -> str:
    # Logic to query Supabase database
    result = "Query result goes here"  # Replace with actual query logic
    return result
mcp.run()
