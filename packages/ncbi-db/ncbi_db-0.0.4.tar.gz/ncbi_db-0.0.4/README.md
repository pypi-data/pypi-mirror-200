# ncbi_db
Collection of scripts that wrap the Entrez Bio python module.
Mainly to build your own copy of selected entries form the ncbi databases


## Installation

conda install -c mmariotti ncbi_db

## Tools

Right now these tools are available:

- *ncbi_assembly*       to browse (and download) the available assemblies/genomes for any species or lineage, including their annotation/proteome
- *ncbi_sequences*      search and download nucleotide/protein sequences or their metadata
- *ncbi_pubmed*         wrapper to ncbi pubmed search engine; it can format results for bibliography
- *ncbi_taxonomy*       search NCBI taxonomy
- *ncbi_taxonomy_tree*  
- *ncbi_db_info*        displays the available fields in any NCBI DB, useful before running ncbi_search
- *ncbi_search*         generic search tool for any NCBI DB
