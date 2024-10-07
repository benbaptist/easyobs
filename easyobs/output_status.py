from dataclasses import dataclass

@dataclass
class OutputStatus:
    type: str
    active: bool = False
    paused: bool = False
    bytes: int = 0
    duration: int = 0
    timecode: str = ""
    skipped_frames: int = 0
    total_frames: int = 0
    congestion: int = 0
    reconnecting: bool = False