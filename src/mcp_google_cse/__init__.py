import asyncio
from . import server


def main():
    """Main entry point for the package."""
    asyncio.run(server.run())


__all__ = ['main', 'server']
