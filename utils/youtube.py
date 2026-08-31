import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_youtube_id(url: str) -> str | None:
    patterns = [
        r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None

def get_transcript(video_id: str) -> str | None:
    try:
        # Instanciamos la clase primero
        api = YouTubeTranscriptApi()
        
        # Usamos el nuevo método list()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(['es', 'es-419', 'en', 'en-US'])
        data = transcript.fetch()
        
        raw_text = " ".join([t.text for t in data])
        return " ".join(raw_text.split())
    except Exception as e:
        print(f"Error obteniendo transcripción ({video_id}): {e}")
        return None