#!/usr/bin/env python3
"""
FPbase GraphQL Provider - Full Implementation v1.3
===================================================

Complete GraphQL harvester with circuit-breaker, pagination, caching, and CSV fallback.

Author: Biological Qubit Atlas Team
License: MIT
"""

import requests
import json
import time
import yaml
from typing import Dict, List, Optional, Any
from pathlib import Path
import sys

# Load config
def load_config() -> Dict[str, Any]:
    """Load provider configuration."""
    config_path = Path("config/providers.yml")
    if not config_path.exists():
        print("ERROR: config/providers.yml not found")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

CONFIG = load_config()
FPBASE_CONFIG = CONFIG['fpbase']

# Configuration
FPBASE_API_URL = FPBASE_CONFIG['api_url']
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Biological-Qubit-Atlas/1.3.0 (research tool)"
}

# Complete GraphQL schema for FPbase
FPBASE_QUERY = """
query GetFluorescentProteins($limit: Int, $offset: Int) {
  fluorescentProteins(first: $limit, offset: $offset) {
    edges {
      node {
        id
        name
        slug
        emMax
        exMax
        brightness
        quantumYield
        extinctionCoefficient
        pka
        maturationTime
        photostability
        oligomericState
        molecularWeight
        aminoAcidLength
        switchType
        isFP
        lifetime
        bleachRate
        structure {
          pdb
          emdb
        }
        references {
          edges {
            node {
              id
              title
              doi
              pmid
              year
            }
          }
        }
      }
    }
  }
}
"""

class CircuitBreaker:
    """Circuit breaker for API calls."""
    
    def __init__(self, failure_threshold: int = 3, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        """Call function with circuit breaker protection."""
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
                print("Circuit breaker: half-open (testing)")
            else:
                raise Exception("Circuit breaker is OPEN (API unavailable)")
        
        try:
            result = func(*args, **kwargs)
            if result.get("status") == "success":
                self.failures = 0
                self.state = "closed"
                return result
            else:
                self._record_failure()
                return result
        except Exception as e:
            self._record_failure()
            raise e
    
    def _record_failure(self):
        """Record a failure."""
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"
            print(f"Circuit breaker: OPEN (failures: {self.failures})")

def fetch_fpbase_page(limit: int = 50, offset: int = 0, circuit_breaker: Optional[CircuitBreaker] = None) -> Dict[str, Any]:
    """
    Fetch one page of fluorescent proteins data from FPbase GraphQL API.
    
    Args:
        limit: Number of proteins to fetch
        offset: Offset for pagination
        circuit_breaker: Optional circuit breaker instance
        
    Returns:
        Dict containing API response or error info
    """
    variables = {
        "limit": limit,
        "offset": offset
    }
    
    payload = {
        "query": FPBASE_QUERY,
        "variables": variables
    }
    
    try:
        response = requests.post(
            FPBASE_API_URL,
            headers=HEADERS,
            json=payload,
            timeout=FPBASE_CONFIG['circuit_breaker']['timeout_seconds']
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "data": data,
                "timestamp": time.time(),
                "offset": offset,
                "limit": limit
            }
        else:
            return {
                "status": "error",
                "error": f"HTTP {response.status_code}: {response.text[:200]}",
                "timestamp": time.time()
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": time.time()
        }

def fetch_fpbase_all(max_proteins: int = 1000) -> Dict[str, Any]:
    """
    Fetch all fluorescent proteins with pagination.
    
    Args:
        max_proteins: Maximum number of proteins to fetch
        
    Returns:
        Dict containing all proteins or error info
    """
    circuit_breaker = CircuitBreaker(
        failure_threshold=FPBASE_CONFIG['circuit_breaker']['failure_threshold'],
        timeout=FPBASE_CONFIG['circuit_breaker']['timeout_seconds']
    )
    
    all_proteins = []
    offset = 0
    batch_size = FPBASE_CONFIG['rate_limit']['max_batch_size']
    max_retries = FPBASE_CONFIG['circuit_breaker']['max_retries']
    retry_delay = FPBASE_CONFIG['circuit_breaker']['retry_delay_seconds']
    
    print(f"Fetching FPbase data (batch_size={batch_size}, max={max_proteins})...")
    
    while offset < max_proteins:
        retries = 0
        while retries < max_retries:
            try:
                result = circuit_breaker.call(fetch_fpbase_page, batch_size, offset)
                
                if result["status"] == "success":
                    edges = result["data"]["data"]["fluorescentProteins"]["edges"]
                    if not edges:
                        print(f"No more proteins at offset {offset}")
                        return {
                            "status": "success",
                            "proteins": all_proteins,
                            "count": len(all_proteins),
                            "timestamp": time.time()
                        }
                    
                    proteins = [edge["node"] for edge in edges]
                    all_proteins.extend(proteins)
                    print(f"OK Fetched {len(proteins)} proteins (total: {len(all_proteins)})")
                    
                    offset += batch_size
                    time.sleep(1)  # Rate limiting
                    break
                else:
                    print(f"ERROR: {result['error']}")
                    retries += 1
                    if retries < max_retries:
                        print(f"Retrying in {retry_delay}s... ({retries}/{max_retries})")
                        time.sleep(retry_delay)
                    else:
                        return result
                        
            except Exception as e:
                print(f"ERROR: Circuit breaker exception: {e}")
                return {
                    "status": "error",
                    "error": str(e),
                    "timestamp": time.time(),
                    "proteins_partial": all_proteins,
                    "count_partial": len(all_proteins)
                }
    
    return {
        "status": "success",
        "proteins": all_proteins,
        "count": len(all_proteins),
        "timestamp": time.time()
    }

def fetch_fpbase_csv_fallback() -> Dict[str, Any]:
    """
    Fallback: fetch FPbase CSV export if GraphQL fails.
    
    Returns:
        Dict containing CSV data or error info
    """
    csv_url = FPBASE_CONFIG['fallback']['csv_url']
    print(f"Trying CSV fallback: {csv_url}")
    
    try:
        response = requests.get(csv_url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            # Save CSV
            output_path = Path("data/raw/fpbase/fpbase_export.csv")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(response.text, encoding='utf-8')
            
            return {
                "status": "success",
                "source": "csv_fallback",
                "path": str(output_path),
                "timestamp": time.time()
            }
        else:
            return {
                "status": "error",
                "error": f"CSV fallback failed: HTTP {response.status_code}",
                "timestamp": time.time()
            }
    except Exception as e:
        return {
            "status": "error",
            "error": f"CSV fallback exception: {e}",
            "timestamp": time.time()
        }

def save_fpbase_full(data: Dict[str, Any]) -> str:
    """
    Save complete FPbase harvest to file.
    
    Args:
        data: Complete FPbase data
        
    Returns:
        Path to saved file
    """
    output_path = Path("data/raw/fpbase/fpbase_full.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return str(output_path)

def main():
    """Main function - full harvest."""
    print("=" * 60)
    print("FPbase GraphQL Provider - Full Harvest v1.3")
    print("=" * 60)
    
    if not FPBASE_CONFIG['enabled']:
        print("ERROR: FPbase provider disabled in config")
        sys.exit(1)
    
    # Try GraphQL first
    result = fetch_fpbase_all(max_proteins=1000)
    
    if result["status"] == "success":
        print(f"OK FPbase GraphQL harvest successful")
        print(f"   Total proteins: {result['count']}")
        
        # Save
        filepath = save_fpbase_full(result)
        print(f"OK Saved to: {filepath}")
        
    else:
        print(f"ERROR FPbase GraphQL failed: {result['error']}")
        
        # Try fallback
        if FPBASE_CONFIG['fallback']['enabled']:
            print("\nTrying CSV fallback...")
            fallback_result = fetch_fpbase_csv_fallback()
            
            if fallback_result["status"] == "success":
                print(f"OK CSV fallback successful: {fallback_result['path']}")
            else:
                print(f"ERROR CSV fallback also failed: {fallback_result['error']}")
                print("\nOutage logged. Continuing with other sources...")
                
                # Log outage
                outage_log = Path(CONFIG['logging']['outage_log'])
                outage_log.parent.mkdir(parents=True, exist_ok=True)
                with open(outage_log, 'a', encoding='utf-8') as f:
                    f.write(f"\n## FPbase Outage - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"- GraphQL Error: {result.get('error', 'unknown')}\n")
                    f.write(f"- CSV Fallback: {fallback_result.get('error', 'unknown')}\n")
                    f.write(f"- Strategy: Continue with specialist DBs + UniProt + PMC\n\n")
                
                print(f"OK Outage logged to: {outage_log}")

if __name__ == "__main__":
    main()
