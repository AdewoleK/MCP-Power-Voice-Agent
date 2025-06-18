from mcp.server import FastMCP
mcp = FastMCP("SupabaseAgent")

@mcp.tool()
def query_database(query: str) -> str:
    # Logic to query Supabase database
    result = "Query result goes here"  # Replace with actual query logic
    return result
mcp.run()

# from mcp.server import FastMCP
# import requests

# mcp = FastMCP("WeatherAgent")

# @mcp.tool()
# def get_weather(city: str) -> str:
#     response = requests.get(f"http://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q={city}")
#     return response.json()['current']['condition']['text']

# mcp.run(port=8000)