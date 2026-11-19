import os
import sys

# Ensure backend directory is in python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from app.main import app

def run_e2e_verification():
    print("==================================================")
    print("AETHERA AI — END-TO-END NEON POSTGRESQL VERIFICATION")
    print("==================================================")
    
    with TestClient(app) as client:
        # 1. Health check
        res_health = client.get("/health")
        assert res_health.status_code == 200, f"Health check failed: {res_health.text}"
        print(f"[PASS] 1. API Health: {res_health.status_code} -> {res_health.json()}")

        # 2. Categories check
        res_cat = client.get("/api/v1/categories")
        assert res_cat.status_code == 200, f"Categories failed: {res_cat.text}"
        cats = res_cat.json()
        assert len(cats) >= 17, f"Expected 17 categories, got {len(cats)}"
        print(f"[PASS] 2. Categories: {res_cat.status_code} -> Successfully retrieved {len(cats)} categories from Neon")

        # 3. Compounds check
        res_comp = client.get("/api/v1/compounds")
        assert res_comp.status_code == 200, f"Compounds failed: {res_comp.text}"
        compounds = res_comp.json()
        assert len(compounds) >= 13, f"Expected 13 compounds, got {len(compounds)}"
        print(f"[PASS] 3. Compounds: {res_comp.status_code} -> Successfully retrieved {len(compounds)} compounds from Neon")

        # 4. Search check (Trigram search on PostgreSQL)
        res_search = client.get("/api/v1/search?q=aspirin")
        assert res_search.status_code == 200, f"Search failed: {res_search.text}"
        results = res_search.json().get("results", [])
        assert len(results) > 0, "Search returned empty results"
        print(f"[PASS] 4. PostgreSQL Trigram Search: Found {len(results)} matches for query 'aspirin' -> {[r['name'] for r in results]}")

        # 5. Compound detail check (Aspirin)
        res_detail = client.get("/api/v1/compounds/aspirin")
        assert res_detail.status_code == 200, f"Compound detail failed: {res_detail.text}"
        data = res_detail.json()
        assert data.get("name") == "Aspirin", f"Unexpected compound name: {data.get('name')}"
        print(f"[PASS] 5. Compound Detail: Aspirin | SMILES={data.get('smiles')} | Formula={data.get('formula')}")

        # 6. Aera AI SSE streaming test
        res_aera = client.post("/api/v1/aera/chat", json={
            "compound_slug": "aspirin",
            "question": "What is the molecular mechanism of Aspirin?"
        })
        assert res_aera.status_code == 200, f"Aera chat failed: {res_aera.text}"
        assert "text/event-stream" in res_aera.headers.get("content-type", "")
        # Read the first few lines of the stream
        preview = res_aera.text[:200].replace("\n", " ")
        print(f"[PASS] 6. Aera AI Real-time Streaming (Groq): {res_aera.status_code} -> Stream connected! Sample: {preview}...")

    print("==================================================")
    print("ALL 6 END-TO-END VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run_e2e_verification()
