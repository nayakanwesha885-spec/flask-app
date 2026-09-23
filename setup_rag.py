from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create the VIDHIVEDA knowledge store
store = client.vector_stores.create(name="VIDHIVEDA Knowledge Base")

print("\nKnowledge store created:")
print(store.name)

# Find all PDFs inside knowledge_base
pdf_files = []

for root, dirs, files in os.walk("knowledge_base"):
    for file in files:
        if file.lower().endswith(".pdf"):
            pdf_files.append(os.path.join(root, file))

print(f"\nFound {len(pdf_files)} PDF file(s).")

# Upload each PDF
for pdf in pdf_files:

    print("\nUploading:")
    print(pdf)

    with open(pdf, "rb") as file_handle:
        uploaded = client.files.create(file=file_handle, purpose="assistants")

    operation = client.vector_stores.files.create(
        vector_store_id=store.id,
        file_id=uploaded.id
    )

    while operation.status not in {"completed", "failed", "cancelled"}:
        time.sleep(3)
        operation = client.vector_stores.files.retrieve(
            vector_store_id=store.id,
            file_id=uploaded.id
        )

    if operation.status != "completed":
        raise RuntimeError(f"Failed to index {pdf}: {operation.status}")

    print("Uploaded successfully!")

# Save the store name into .env
with open(".env", "a") as env_file:
    env_file.write(
        f"\nOPENAI_VECTOR_STORE_ID={store.id}\n"
    )

print("\n================================")
print("VIDHIVEDA KNOWLEDGE BASE READY")
print("================================")
print("Store:", store.name)
print(f"Total PDFs: {len(pdf_files)}")