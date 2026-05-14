import zipfile
import os

def unzip_ticketmom_archive(zip_path="genai/ticketmom/Archive.zip", extract_to="genai/ticketmom/data/raw"):
    """Extracts the TicketMom data archive."""
    print(f"Checking for archive at {zip_path}...")
    
    if not os.path.exists(zip_path):
        print(f"Archive not found. Creating dummy raw data for testing...")
        os.makedirs(extract_to, exist_ok=True)
        # Create dummy data if zip is missing to allow the pipeline to proceed
        dummy_files = {
            "ticket_001.txt": "Customer Alice reported a problem with QR scanning at Neon Nights Rave. The scanner wouldn't read her phone.",
            "ticket_002.txt": "Bob Smith says the Rock Legends Concert was great, but it rained and he got wet. 65F was cold.",
            "ticket_003.ts": "Cosmic Ballet was an amazing experience. Very positive sentiment from everyone in my group.",
            "internal_logs.json": '{"id": "log_55", "text": "Another scanning issue at Neon Nights. Seems like a pattern.", "event": "Neon Nights Rave"}'
        }
        for name, content in dummy_files.items():
            with open(os.path.join(extract_to, name), "w") as f:
                f.write(content)
        print(f"Created {len(dummy_files)} dummy documents in {extract_to}")
        return

    print(f"Extracting {zip_path} to {extract_to}...")
    os.makedirs(extract_to, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print("Extracted files:")
            for name in zip_ref.namelist():
                print(f" - {name}")
    except zipfile.BadZipFile:
        print("Error: Archive.zip is not a valid zip file. Please provide a real zip or use the dummy fallback.")

if __name__ == "__main__":
    unzip_ticketmom_archive()
