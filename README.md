# Virus Stereopointer

Demo for adding a Loculus and Genspectrum linkout, based on: https://github.com/cbg-ethz/v-pipe-scout/issues/115.

```
https://swissmodel.expasy.org/repository/uniprot/{protein_name}?annot={query}
```

Where:

protein_name = UniProt accession (e.g., "P0DTC2" for Spike)
query = gzip-compressed, base64-encoded annotation table
Annotation Format:
{protein_name} {start_pos} {end_pos} {color} {reference} {annotation}


protein_name=A0A482JPF1