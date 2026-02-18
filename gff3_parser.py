#!/usr/bin/env python3

import pandas as pd
import requests

def get_uniprotKB_id(protein_id):
    params = {
    "query": protein_id,
    "fields": [
        "accession"
    ],
    "size": "50"
    }
    headers = {
    "accept": "application/json"
    }
    base_url = "https://rest.uniprot.org/uniparc/search"

    response = requests.get(base_url, headers=headers, params=params)
    if not response.ok:
        response.raise_for_status()

    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        result = data["results"][0]
        if "uniProtKBAccessions" in result and len(result["uniProtKBAccessions"]) > 0:
            return result["uniProtKBAccessions"][0]
        else:
            return None
    else:
        return None

cols = ["seqid","source","type","start","end","score","strand","phase","attributes"]
df = pd.read_csv("covid.gff3", sep="\t", comment="#", names=cols)
df_filtered = df[(df.type == "CDS") | (df.type == "mature_protein_region_of_CDS")]
# extract product, protein_id, Parent and ID from attributes
df_filtered["product"] = df_filtered.attributes.str.extract(r"product=([^;]+)")
df_filtered["protein_id"] = df_filtered.attributes.str.extract(r"protein_id=([^;]+)")
df_filtered["Parent"] = df_filtered.attributes.str.extract(r"Parent=([^;]+)")
df_filtered["ID"] = df_filtered.attributes.str.extract(r"ID=([^;]+)")
df_filtered["uniprotKB_id"] = df_filtered.protein_id.apply(get_uniprotKB_id)
print(df_filtered)