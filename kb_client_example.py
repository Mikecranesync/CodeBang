"""
Example KB Client Implementation for DevCTO Agent

This file shows how the kb_client module should be implemented
when Phase 2-3 are started. Place this in src/kb_client/client.py

Key features:
- Connects to Agent-Factory KB API
- Provides bootstrap helper for core DevCTO atoms
- Caches responses to reduce API calls
- Handles errors gracefully
"""

import requests
from typing import List, Dict, Optional
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class KBClient:
    """
    Client for querying the Agent-Factory knowledge base.

    Usage:
        kb = KBClient("http://localhost:8000")
        atoms = kb.search("testing patterns", top_k=5)
        bootstrap = kb.get_devcto_bootstrap_atoms()
    """

    def __init__(self, agent_factory_url: str, timeout: int = 30):
        """
        Initialize KB client.

        Args:
            agent_factory_url: Base URL of Agent-Factory API
            timeout: Request timeout in seconds
        """
        self.base_url = agent_factory_url.rstrip('/')
        self.timeout = timeout
        self._cache = {}

        # Verify connection on init
        try:
            self._health_check()
        except Exception as e:
            logger.warning(f"KB health check failed: {e}")

    def _health_check(self):
        """Verify Agent-Factory API is accessible"""
        try:
            resp = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Cannot connect to Agent-Factory at {self.base_url}: {e}")

    def search(self, query: str, top_k: int = 5, use_cache: bool = True) -> List[Dict]:
        """
        Search the knowledge base for relevant atoms.

        Args:
            query: Search query string
            top_k: Number of results to return
            use_cache: Whether to use cached results

        Returns:
            List of atom dictionaries with id, summary, content, etc.

        Example:
            atoms = kb.search("testing patterns", top_k=5)
            for atom in atoms:
                print(f"{atom['id']}: {atom['summary']}")
        """
        cache_key = f"search:{query}:{top_k}"

        if use_cache and cache_key in self._cache:
            logger.debug(f"Cache hit for query: {query}")
            return self._cache[cache_key]

        try:
            resp = requests.post(
                f"{self.base_url}/api/kb/search",
                json={"query": query, "top_k": top_k},
                timeout=self.timeout
            )
            resp.raise_for_status()
            atoms = resp.json()["atoms"]

            # Cache the results
            self._cache[cache_key] = atoms

            logger.info(f"KB search for '{query}' returned {len(atoms)} atoms")
            return atoms

        except requests.exceptions.RequestException as e:
            logger.error(f"KB search failed for '{query}': {e}")
            return []

    def get_atom(self, atom_id: str, use_cache: bool = True) -> Optional[Dict]:
        """
        Fetch a specific atom by ID.

        Args:
            atom_id: Unique atom identifier
            use_cache: Whether to use cached atom

        Returns:
            Atom dictionary or None if not found

        Example:
            atom = kb.get_atom("devcto_core_loop")
            print(atom["summary"])
        """
        cache_key = f"atom:{atom_id}"

        if use_cache and cache_key in self._cache:
            logger.debug(f"Cache hit for atom: {atom_id}")
            return self._cache[cache_key]

        try:
            resp = requests.get(
                f"{self.base_url}/api/kb/atom",
                params={"atom_id": atom_id},
                timeout=self.timeout
            )
            resp.raise_for_status()
            atom = resp.json()["atom"]

            # Cache the atom
            self._cache[cache_key] = atom

            logger.info(f"Fetched atom: {atom_id}")
            return atom

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch atom '{atom_id}': {e}")
            return None

    def get_devcto_bootstrap_atoms(self) -> List[Dict]:
        """
        Fetch core DevCTO atoms needed for bootstrapping.

        This is a convenience method that retrieves the essential atoms
        that any DevCTO development work should consult first.

        Returns:
            List of core DevCTO atoms

        Example:
            atoms = kb.get_devcto_bootstrap_atoms()
            for atom in atoms:
                print(f"{atom['id']}: {atom['summary']}")
        """
        core_atom_ids = [
            "devcto_core_loop",
            "devcto_repo_structure",
            "devcto_guardrails_philosophy",
            "devcto_kb_integration",
            "devcto_headless_exec",
            "devcto_analyzer_pattern",
            "devcto_executor_pattern",
            "devcto_learning_loop"
        ]

        atoms = []
        for atom_id in core_atom_ids:
            atom = self.get_atom(atom_id)
            if atom:
                atoms.append(atom)
            else:
                logger.warning(f"Core atom not found: {atom_id}")

        logger.info(f"Loaded {len(atoms)}/{len(core_atom_ids)} bootstrap atoms")
        return atoms

    def search_by_namespace(self, namespace: str, top_k: int = 20) -> List[Dict]:
        """
        Search for all atoms in a specific namespace.

        Args:
            namespace: Namespace prefix (e.g., "devcto", "langfuse")
            top_k: Maximum results to return

        Returns:
            List of atoms matching the namespace

        Example:
            devcto_atoms = kb.search_by_namespace("devcto", top_k=20)
        """
        return self.search(f"{namespace}_", top_k=top_k)

    def ingest_source(self, url: str, source_type: str = "github") -> Optional[str]:
        """
        Trigger ingestion of a new source into the knowledge base.

        Args:
            url: URL of the source to ingest
            source_type: Type of source (github, article, documentation)

        Returns:
            Job ID for tracking ingestion progress, or None if failed

        Example:
            job_id = kb.ingest_source(
                "https://github.com/example/repo",
                source_type="github"
            )
        """
        try:
            resp = requests.post(
                f"{self.base_url}/api/ingest",
                json={"url": url, "source_type": source_type},
                timeout=self.timeout
            )
            resp.raise_for_status()
            job_id = resp.json()["job_id"]

            logger.info(f"Triggered ingestion of {url} (job: {job_id})")
            return job_id

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to trigger ingestion for {url}: {e}")
            return None

    def clear_cache(self):
        """Clear the response cache"""
        self._cache.clear()
        logger.info("KB client cache cleared")

    def get_stats(self) -> Dict:
        """Get KB statistics and metadata"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/kb/stats",
                timeout=self.timeout
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch KB stats: {e}")
            return {"error": str(e)}


# Example usage and testing
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Initialize client
    kb = KBClient("http://localhost:8000")

    # Bootstrap example
    print("=== Bootstrap DevCTO Atoms ===")
    atoms = kb.get_devcto_bootstrap_atoms()
    for atom in atoms:
        print(f"\n{atom['id']}:")
        print(f"  Summary: {atom.get('summary', 'N/A')}")
        print(f"  When to use: {atom.get('when_to_use', 'N/A')[:100]}...")

    # Search example
    print("\n=== Search for Testing Patterns ===")
    results = kb.search("testing patterns", top_k=3)
    for result in results:
        print(f"- {result['id']}: {result.get('summary', 'N/A')}")

    # Specific atom example
    print("\n=== Fetch Specific Atom ===")
    atom = kb.get_atom("devcto_core_loop")
    if atom:
        print(f"ID: {atom['id']}")
        print(f"Summary: {atom.get('summary', 'N/A')}")

    # Stats example
    print("\n=== KB Statistics ===")
    stats = kb.get_stats()
    print(f"Total atoms: {stats.get('total_atoms', 'unknown')}")
    print(f"Namespaces: {stats.get('namespaces', 'unknown')}")
