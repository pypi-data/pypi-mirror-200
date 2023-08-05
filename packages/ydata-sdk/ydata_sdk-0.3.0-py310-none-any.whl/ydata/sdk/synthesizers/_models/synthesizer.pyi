from typing import Dict, Optional

class Synthesizer:
    uid: Optional[str]
    author: Optional[str]
    name: Optional[str]
    status: Optional[Dict]
    def __init__(self, uid, author, name, status) -> None: ...
