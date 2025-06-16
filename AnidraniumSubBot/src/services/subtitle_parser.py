"""
Парсер субтитров для обработки файлов SRT и VTT форматов.
"""

import re
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
import chardet

@dataclass
class SubtitleEntry:
    start_time: str
    end_time: str
    text: str
    duration: float

class SubtitleParser:
    def __init__(self):
        pass

    def parse_file(self, file_path: str) -> List[SubtitleEntry]:
        encoding = self._detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        fmt = self._detect_format(file_path)
        if fmt == "srt":
            return self._parse_srt(content)
        elif fmt == "vtt":
            return self._parse_vtt(content)
        else:
            raise ValueError("Unknown subtitle format")

    def _detect_format(self, file_path: str) -> str:
        if file_path.endswith(".srt"):
            return "srt"
        elif file_path.endswith(".vtt"):
            return "vtt"
        else:
            return "unknown"

    def _detect_encoding(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            raw = f.read(4096)
            result = chardet.detect(raw)
            return result['encoding'] or 'utf-8'

    def _parse_srt(self, content: str) -> List[SubtitleEntry]:
        # Простой парсер SRT для примера
        entries = []
        blocks = re.split(r'\n\s*\n', content.strip())
        for block in blocks:
            lines = block.splitlines()
            if len(lines) >= 3:
                times = lines[1]
                start, end = times.split(" --> ")
                text = " ".join(lines[2:])
                duration = self._duration_from_timestamps(start, end)
                entries.append(SubtitleEntry(start, end, self._clean_text(text), duration))
        return self._merge_short_entries(entries)

    def _parse_vtt(self, content: str) -> List[SubtitleEntry]:
        entries = []
        blocks = re.split(r'\n\s*\n', content.strip())
        for block in blocks:
            lines = block.splitlines()
            if len(lines) >= 2 and "-->" in lines[0]:
                times = lines[0]
                start, end = times.split(" --> ")
                text = " ".join(lines[1:])
                duration = self._duration_from_timestamps(start, end)
                entries.append(SubtitleEntry(start, end, self._clean_text(text), duration))
        return self._merge_short_entries(entries)

    def _clean_text(self, text: str) -> str:
        return re.sub(r'<.*?>', '', text).replace('\n', ' ').strip()

    def _merge_short_entries(self, entries: List[SubtitleEntry]) -> List[SubtitleEntry]:
        # Пример объединения коротких фраз
        merged = []
        buf = []
        for entry in entries:
            if len(entry.text) < 15:
                buf.append(entry)
                continue
            if buf:
                combined = " ".join(e.text for e in buf) + " " + entry.text
                merged.append(SubtitleEntry(buf[0].start_time, entry.end_time, combined, entry.duration))
                buf = []
            else:
                merged.append(entry)
        return merged

    def _duration_from_timestamps(self, start: str, end: str) -> float:
        def to_seconds(ts):
            h, m, s = re.split('[:,]', ts)
            return int(h)*3600 + int(m)*60 + float(s)
        return to_seconds(end.strip()) - to_seconds(start.strip())

    def get_statistics(self, entries: List[SubtitleEntry]) -> Dict[str, Any]:
        return {
            "blocks": len(entries),
            "duration": sum(e.duration for e in entries)
        }

    def format_for_ai(self, entries: List[SubtitleEntry]) -> str:
        return "\n".join(f"{e.start_time} - {e.end_time}: {e.text}" for e in entries)