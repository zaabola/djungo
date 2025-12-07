from mcp.server.fastmcp import FastMCP
# Create an instance of FastMCP
# All parameters are optional
mcp = FastMCP(
name="MyCalculator"
)
@mcp.tool()
def say_hello(name : str) -> str:

    return "Hello World ! "+ name

@mcp.tool()
def addition(a: float, b: float) -> float:
    """Addition de deux nombres"""
    return a + b

@mcp.tool()
def soustraction(a: float, b: float) -> float:
    """Soustraction de deux nombres"""
    return a - b

@mcp.tool()
def multiplication(a: float, b: float) -> float:
    """Multiplication de deux nombres"""
    return a * b

@mcp.tool()
def division(a: float, b: float) -> float:
    """Division de deux nombres"""
    if b == 0:
        raise ValueError("Division par zéro non autorisée")
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")
# You can change transport to "sse" if needed