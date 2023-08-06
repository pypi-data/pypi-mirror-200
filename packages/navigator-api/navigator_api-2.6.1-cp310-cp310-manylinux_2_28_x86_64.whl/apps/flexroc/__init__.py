"""
Program Init.

Flexroc Program.
"""
from resources.program import ProgramConfig

class flexroc(ProgramConfig):
    __version__ = '0.0.1'
    app_description = """
    API for FLEXROC
    """
    program_slug: str = 'flexroc'
