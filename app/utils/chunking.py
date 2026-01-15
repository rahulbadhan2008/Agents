from typing import List
import re

class ChunkingUtility:
    @staticmethod
    def split_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into chunks with specified size and overlap."""
        if not text:
            return []
            
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at a newline or period if possible to maintain semantic integrity
            if end < len(text):
                last_space = chunk.rfind(' ')
                if last_space != -1:
                    chunk = chunk[:last_space]
                    end = start + last_space
            
            chunks.append(chunk.strip())
            start = end - overlap
            
            if start < 0: # Safety break
                start = end
                
        return chunks

    @staticmethod
    def clean_text(text: str) -> str:
        """Simple cleaning of the text."""
        # Remove multiple newlines and spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

chunking_utility = ChunkingUtility()
