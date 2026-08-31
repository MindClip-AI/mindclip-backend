import os

from dotenv import load_dotenv
from supabase import Client, create_client

from utils.youtube import extract_youtube_id, get_transcript

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def process_pending_videos() -> None:
    response = (
        supabase.table("contents")
        .select("*")
        .eq("status", "processing")
        .eq("source_type", "youtube")
        .execute()
    )

    records = response.data or []

    if not records:
        print("No hay videos pendientes por procesar.")
        return

    for record in records:
        youtube_id = extract_youtube_id(record["source_url"])
        print(f"Procesando ID Contenido: {record['id']} | YouTube ID: {youtube_id}")

        transcript_text = get_transcript(youtube_id) if youtube_id else None

        if transcript_text:
            (
                supabase.table('contents')
                .update({'transcript': transcript_text})
                .eq('id', record['id'])
                .execute()
            )
            print(f"Transcripción guardada para {record['id']} (Longitud: {len(transcript_text)} caracteres)")
        else:
            (
                supabase.table('contents')
                .update({'status': 'failed'})
                .eq('id', record['id'])
                .execute()
            )
            print(f"Error: No se pudo obtener transcripción para {record['id']}. Marcat como 'failed'")


if __name__ == "__main__":
    process_pending_videos()