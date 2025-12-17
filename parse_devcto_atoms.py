"""
DevCTO Atom Parser

Parses DEVCTO_CLAUDE_ATOMS.md into structured atoms ready for database ingestion.

Extracts:
- atom_id from ## Atom: header
- title (cleaned version of atom_id)
- summary from **Summary:** section
- content (full atom markdown)
- keywords from **Key concepts:** section
- related_atoms from **Related atoms:** section

Generates OpenAI embeddings for vector search.

Usage:
    from parse_devcto_atoms import parse_devcto_atoms
    atoms = parse_devcto_atoms("DEVCTO_CLAUDE_ATOMS.md")
    print(f"Parsed {len(atoms)} atoms")
"""

import os
import re
import uuid
from pathlib import Path
from typing import Dict, List

import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_devcto_atoms(file_path: str) -> List[Dict]:
    """
    Parse DEVCTO_CLAUDE_ATOMS.md into structured atoms.

    Args:
        file_path: Path to DEVCTO_CLAUDE_ATOMS.md

    Returns:
        List of atom dictionaries ready for database insertion

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If OpenAI API key not set
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set")

    # Read file
    content = Path(file_path).read_text(encoding='utf-8')

    # Split by atom boundaries (---)
    atom_sections = re.split(r'^---\s*$', content, flags=re.MULTILINE)

    atoms = []
    processed_count = 0

    for section in atom_sections:
        if not section.strip() or '## Atom:' not in section:
            continue

        # Extract atom_id
        atom_match = re.search(r'## Atom:\s+(\w+)', section)
        if not atom_match:
            print(f"Warning: Skipping section without atom ID")
            continue

        atom_id = atom_match.group(1)
        print(f"Processing: {atom_id}")

        # Extract fields
        summary_match = re.search(
            r'\*\*Summary:\*\*\s+(.+?)(?=\n\n\*\*|$)',
            section,
            re.DOTALL
        )
        when_to_use_match = re.search(
            r'\*\*When to use:\*\*\s+(.+?)(?=\n\n\*\*|$)',
            section,
            re.DOTALL
        )
        key_concepts_match = re.search(
            r'\*\*Key concepts:\*\*\s+(.+?)(?=\n\n\*\*|$)',
            section,
            re.DOTALL
        )
        related_match = re.search(
            r'\*\*Related atoms:\*\*\s+(.+?)(?=\n|$)',
            section
        )
        source_match = re.search(
            r'\*\*Source:\*\*\s+(.+?)(?=\n|$)',
            section
        )

        # Build content (combine all sections)
        content_parts = []

        if summary_match:
            content_parts.append(f"Summary: {summary_match.group(1).strip()}")

        if when_to_use_match:
            content_parts.append(f"\n\nWhen to use:\n{when_to_use_match.group(1).strip()}")

        if key_concepts_match:
            content_parts.append(f"\n\nKey concepts:\n{key_concepts_match.group(1).strip()}")

        # Add code patterns if present
        code_pattern_match = re.search(
            r'\*\*Code pattern:\*\*\s+(.+?)(?=\n\n\*\*|$)',
            section,
            re.DOTALL
        )
        if code_pattern_match:
            content_parts.append(f"\n\nCode pattern:\n{code_pattern_match.group(1).strip()}")

        # Add implementation notes if present
        impl_notes_match = re.search(
            r'\*\*Implementation notes:\*\*\s+(.+?)(?=\n\n\*\*|$)',
            section,
            re.DOTALL
        )
        if impl_notes_match:
            content_parts.append(f"\n\nImplementation notes:\n{impl_notes_match.group(1).strip()}")

        # Add API endpoints if present
        api_endpoints_match = re.search(
            r'\*\*API endpoints required:\*\*\s+(.+?)(?=\n\n\*\*|$)',
            section,
            re.DOTALL
        )
        if api_endpoints_match:
            content_parts.append(f"\n\nAPI endpoints:\n{api_endpoints_match.group(1).strip()}")

        # Add best practices if present
        best_practices_match = re.search(
            r'\*\*Best practices:\*\*\s+(.+?)(?=\n\n\*\*|$)',
            section,
            re.DOTALL
        )
        if best_practices_match:
            content_parts.append(f"\n\nBest practices:\n{best_practices_match.group(1).strip()}")

        # Extract keywords from key concepts
        keywords = []
        if key_concepts_match:
            concepts_text = key_concepts_match.group(1).strip()
            # Extract bullet points
            concepts = re.findall(r'^[-•]\s*(.+?)$', concepts_text, re.MULTILINE)
            keywords = [c.split(':')[0].strip() for c in concepts if c.strip()]

        # Extract related atoms
        related_atoms = []
        if related_match:
            related_text = related_match.group(1).strip()
            # Extract atom IDs from backticks
            related_atoms = re.findall(r'`([^`]+)`', related_text)

        # Build full content
        full_content = '\n'.join(content_parts)

        # Generate embedding
        print(f"  Generating embedding for {atom_id}...")
        try:
            embedding_response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=f"{atom_id}: {summary_match.group(1).strip() if summary_match else ''}"
            )
            embedding = embedding_response.data[0].embedding
        except Exception as e:
            print(f"  Warning: Failed to generate embedding for {atom_id}: {e}")
            # Use empty embedding as fallback (will need to be regenerated)
            embedding = [0.0] * 1536

        # Build atom dictionary
        atom = {
            "id": str(uuid.uuid4()),
            "atom_id": atom_id,
            "atom_type": "pattern",
            "title": atom_id.replace('_', ' ').title(),
            "summary": summary_match.group(1).strip() if summary_match else "",
            "content": full_content,
            "manufacturer": "devcto",
            "product_family": "agent",
            "product_version": "v1.0",
            "difficulty": "intermediate",
            "prerequisites": [],  # Could be inferred from related_atoms
            "related_atoms": related_atoms,
            "source_document": "DEVCTO_CLAUDE_ATOMS.md",
            "source_pages": [1],
            "keywords": keywords,
            "quality_score": 1.0,  # Hand-crafted, high quality
            "embedding": embedding
        }

        atoms.append(atom)
        processed_count += 1
        print(f"  [OK] Processed {atom_id}")

    print(f"\nParsed {processed_count} atoms successfully")
    return atoms


if __name__ == "__main__":
    import sys

    # Default path
    default_path = "C:\\Users\\hharp\\OneDrive\\Desktop\\CodeBang\\DEVCTO_CLAUDE_ATOMS.md"
    file_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    print(f"Parsing DevCTO atoms from: {file_path}\n")

    try:
        atoms = parse_devcto_atoms(file_path)

        print(f"\n{'='*60}")
        print("PARSED ATOMS SUMMARY")
        print(f"{'='*60}")

        for atom in atoms:
            print(f"\n{atom['atom_id']}:")
            print(f"  Title: {atom['title']}")
            print(f"  Summary: {atom['summary'][:80]}...")
            print(f"  Keywords: {', '.join(atom['keywords'][:3])}...")
            print(f"  Related: {', '.join(atom['related_atoms'][:3])}...")
            print(f"  Embedding dims: {len(atom['embedding'])}")

        print(f"\n{'='*60}")
        print(f"Total atoms parsed: {len(atoms)}")
        print(f"{'='*60}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
