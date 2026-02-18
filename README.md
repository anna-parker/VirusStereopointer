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

We would like to generate a structure like the following from a GFF3:
```
polyprotein_to_mature: {
    "ORF1a": [
        {
            poly_start:266,
            poly_end: 13483,
            mature_name: "Orf1a_snip",
            mature_start: 1
        },
    ],
    "ORF1b": [
    ]
},
uniprot_ref: {
    'F':"A0A482JPF1",
    'Orf1a_snip':"A0A482JPF1",
    'Orf1a_snip2':"A0A482JPF1",
},
mature_lengths: {
    '3CLPro': 306, # use product as name
    'RdRp': 933,
},
```

Get the UniProtKB Id from the gff3 `protein_id` using 
```
curl -X 'GET' \
  'https://rest.uniprot.org/uniprotkb/search?query=YP_009742612.1&fields=accession&sort=accession%20desc&size=50' \
  -H 'accept: application/json'
```
Typical result if valid:
```
{
  "results": [
    {
      "entryType": "UniProtKB unreviewed (TrEMBL)",
      "primaryAccession": "A0ABF7SXH4",
      "extraAttributes": {
        "uniParcId": "UPI00137481FB"
      }
    }
  ]
}
```
If there are multiple results or no results this indicates there is no 3D structure.

Alternatively try: 
```
curl -X 'GET' \
  'https://rest.uniprot.org/uniparc/search?query=WBQ20026.1&fields=accession&size=50' \
  -H 'accept: application/json'
```
and use one of the `UniProtKB` accessions:
```
{
  "results": [
    {
      "uniParcId": "UPI000BBF9456",
      "uniProtKBAccessions": [
        "A0A482JPF1",
        "A0A292GCX4",
        "A0A7D5D2B8"
      ],
      "oldestCrossRefCreated": "2017-10-05",
      "mostRecentCrossRefUpdated": "2026-01-28"
    }
  ]
}
```

