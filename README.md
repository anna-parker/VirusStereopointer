# Virus Stereopointer

Demo for adding a Loculus and Genspectrum linkout, based on: https://github.com/cbg-ethz/v-pipe-scout/issues/115.

```
https://swissmodel.expasy.org/repository/uniprot/{protein_name}?annot={query}
```
Where:

protein_name = UniProt accession (e.g., "P0DTC2" for Spike)
query = gzip-compressed, base64-encoded annotation table

### Annotation Format:
```
{protein_name} {start_pos} {end_pos} {color} {reference} {annotation}
```

### How to get the protein name?
```
protein_name=A0A482JPF1
```

Take the gff3 and look for CDS or mature_protein_region_of_cds and get the `protein_id=YP_009742612.1`, then you can search in UniProtKB for the UnitProt ID, e.g.:  https://www.uniprot.org/uniprotkb?query=YP_009742612.1 - this is what would be used as the `protein_name`, e.g. `A0ABF7SXH4`.

For SARS-COV2 we do not have the mature proteins but the presliced CDS so we need to get the AA mutations of the CDS and then map to the mature protein. 

Look at `gene=ORF1ab`, there are 2 CDSs for this, one with ribosomal slippage. In real life you would get 2 different products ORF1a or if the ribosome did not slip it will "skip" a stop codon and keep transcribing into sth called ORF1ab. In CovSpectrum and nextclade ORF1a and ORF1b have been split up: https://github.com/nextstrain/nextclade_data/blob/master/data/nextstrain/sars-cov-2/wuhan-hu-1/orfs/genome_annotation.gff3. 

ORF1ab and ORF1a are both "pre-sliced" genes which means for the proteins we are interested in the final products. 

