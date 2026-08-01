from app.services.chunking_service import ChunkingService

text = "A" * 3500

chunker = ChunkingService()

chunks = chunker.chunk_text(text)

print("Chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(i + 1, len(chunk))