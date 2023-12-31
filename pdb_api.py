# Import necessary libraries
import requests
import sys
import os
from Bio.PDB import PDBList, PDBParser

# Function to get protein information from the RCSB PDB API
def get_protein_info(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()  # Raises exception for 4xx or 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to list available API calls for a given PDB ID
def list_available_api_calls(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()  # Raises exception for 4xx or 5xx status codes
        data = response.json()
        return data.keys()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to get FASTA sequence from the RCSB PDB API
def get_fasta_sequence(pdb_id):
    url = f"https://www.rcsb.org/fasta/entry/{pdb_id}"
    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()  # Raises exception for 4xx or 5xx status codes
        fasta_data = response.text
        return fasta_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Main function
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the PDB ID as a runtime argument.")
        sys.exit(1)
    pdb_id = sys.argv[1]
    
    # Get protein information and print specific details
    protein_info = get_protein_info(pdb_id)
    if protein_info:
        if 'rcsb_id' in protein_info:
            print(f"Protein ID: {protein_info['rcsb_id']}")
        if 'struct' in protein_info and 'title' in protein_info['struct']:
            print(f"Title: {protein_info['struct']['title']}")
        if 'exptl' in protein_info and len(protein_info['exptl']) > 0 and 'method' in protein_info['exptl'][0]:
            print(f"Experimental Method: {protein_info['exptl'][0]['method']}")
        if 'rcsb_entry_info' in protein_info and 'resolution_combined' in protein_info['rcsb_entry_info']:
            print(f"Resolution: {protein_info['rcsb_entry_info']['resolution_combined']} angstroms")
    else:
        print("Failed to retrieve protein information.\n")

    # List available API calls for the given PDB ID
    available_api_calls = list_available_api_calls(pdb_id)
    if available_api_calls:
        print("\nAvailable API calls for the given PDB ID:")
        for api_call in available_api_calls:
            print(api_call)
        print("\n")
    else:
        print("Failed to retrieve available API calls.\n")
    
    # Get and print the FASTA sequence for the given PDB ID
    fasta_sequence = get_fasta_sequence(pdb_id)
    if fasta_sequence:
        print(f"Fasta Sequence for PDB ID {pdb_id}:")
        print(fasta_sequence)
    else:
        print("Failed to retrieve FASTA sequence.")
