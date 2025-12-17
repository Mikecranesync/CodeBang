"""
DevCTO Atom Ingestion Script

Ingests the 14 DevCTO learning atoms into Agent-Factory knowledge base.

Process:
1. Parse DEVCTO_CLAUDE_ATOMS.md using parse_devcto_atoms.py
2. Connect to Supabase via Agent-Factory storage
3. Insert each atom into knowledge_atoms table
4. Verify ingestion success

Usage:
    python ingest_devcto_atoms.py

Requirements:
    - Agent-Factory in Python path
    - SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in environment
    - OPENAI_API_KEY for embeddings

Output:
    - Progress messages for each atom
    - Success/failure summary
    - Verification of atom count in database
"""

import os
import sys
from pathlib import Path

# Add Agent-Factory to path
agent_factory_path = Path("C:/Users/hharp/OneDrive/Desktop/Agent Factory")
if agent_factory_path.exists():
    sys.path.insert(0, str(agent_factory_path))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import parser
from parse_devcto_atoms import parse_devcto_atoms


def ingest_devcto_atoms():
    """
    Ingest DevCTO atoms into Agent-Factory knowledge base.

    Returns:
        Tuple of (success_count, failure_count, total_atoms)
    """
    print("=" * 70)
    print("DevCTO Atom Ingestion")
    print("=" * 70)

    # Step 1: Parse atoms
    print("\n[1/4] Parsing DEVCTO_CLAUDE_ATOMS.md...")
    atoms_file = "C:/Users/hharp/OneDrive/Desktop/CodeBang/DEVCTO_CLAUDE_ATOMS.md"

    try:
        atoms = parse_devcto_atoms(atoms_file)
        print(f"✓ Parsed {len(atoms)} atoms\n")
    except Exception as e:
        print(f"✗ Failed to parse atoms: {e}")
        return 0, 0, 0

    # Step 2: Connect to storage
    print("[2/4] Connecting to Agent-Factory storage...")
    try:
        from agent_factory.memory.storage import SupabaseMemoryStorage
        storage = SupabaseMemoryStorage()
        print("✓ Connected to Supabase\n")
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        print("\nTroubleshooting:")
        print("- Check SUPABASE_URL is set")
        print("- Check SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_KEY) is set")
        print("- Verify Agent-Factory is in Python path")
        return 0, len(atoms), len(atoms)

    # Step 3: Insert atoms
    print("[3/4] Inserting atoms into knowledge_atoms table...")
    success_count = 0
    failure_count = 0

    for atom in atoms:
        try:
            # Insert atom
            response = storage.client.table("knowledge_atoms").insert(atom).execute()

            print(f"  ✓ {atom['atom_id']}")
            success_count += 1

        except Exception as e:
            print(f"  ✗ {atom['atom_id']}: {e}")
            failure_count += 1

    print(f"\nIngestion complete: {success_count}/{len(atoms)} successful\n")

    # Step 4: Verify
    print("[4/4] Verifying ingestion...")
    try:
        result = storage.client.table("knowledge_atoms")\
            .select("atom_id")\
            .eq("manufacturer", "devcto")\
            .execute()

        verified_count = len(result.data)
        print(f"✓ Verified: {verified_count} DevCTO atoms in database\n")

        if verified_count == len(atoms):
            print("✓ All atoms verified successfully!")
        else:
            print(f"⚠ Expected {len(atoms)} atoms, found {verified_count}")

        # List all ingested atoms
        print("\nIngested atoms:")
        for atom_data in result.data:
            print(f"  - {atom_data['atom_id']}")

    except Exception as e:
        print(f"✗ Verification failed: {e}")

    print("\n" + "=" * 70)
    print(f"SUMMARY: {success_count} succeeded, {failure_count} failed")
    print("=" * 70)

    return success_count, failure_count, len(atoms)


def check_existing_atoms():
    """
    Check if DevCTO atoms already exist in database.

    Returns:
        Number of existing DevCTO atoms
    """
    try:
        from agent_factory.memory.storage import SupabaseMemoryStorage
        storage = SupabaseMemoryStorage()

        result = storage.client.table("knowledge_atoms")\
            .select("atom_id")\
            .eq("manufacturer", "devcto")\
            .execute()

        return len(result.data)

    except Exception as e:
        print(f"Could not check existing atoms: {e}")
        return 0


def main():
    """Main ingestion workflow"""
    print("\nChecking for existing DevCTO atoms...")
    existing_count = check_existing_atoms()

    if existing_count > 0:
        print(f"Found {existing_count} existing DevCTO atoms in database.")
        response = input("Do you want to proceed? This may create duplicates. (yes/no): ")

        if response.lower() not in ['yes', 'y']:
            print("Ingestion cancelled.")
            return

    # Run ingestion
    success, failed, total = ingest_devcto_atoms()

    # Exit code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
