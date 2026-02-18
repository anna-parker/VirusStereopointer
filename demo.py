#!/usr/bin/env python3

import pandas as pd
import re
import colorsys
import gzip
import base64

rx_pos = re.compile(r"^(?P<prot>[A-Z]):(?P<mutFrom>[A-Z\*])(?P<pos>\d+)(?P<mutTo>[A-Z\*])$")

protein_name= {"F":"A0A482JPF1"}
lengths = {"F": (7421 - 5697 + 1)/3 }

df = pd.read_csv("rsv-mutations-over-time.csv", header=0, index_col='mutation')
average = df[df.columns].mean(axis=1)
newindex = average.index.str.extract(rx_pos)
average.index = newindex
print(average)

def to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*[int(val*255) for val in rgb])

def create_csv_entry(
    prot,mutFrom, pos, mutTo, frequency
):
    print(prot, mutFrom, pos, mutTo, frequency)
    # {protein_name} {start_pos} {end_pos} {color} {reference} {annotation}
    return f"{protein_name[prot]}\t{pos}\t{pos}\t{to_hex(colorsys.hsv_to_rgb(int(pos)/lengths[prot], frequency, 1))}\tGenSpectrum\t{mutFrom}{pos}{mutTo}"

csv_content="\n".join([create_csv_entry(*idx, val) for idx, val in average.items()])
byte_object = gzip.compress(csv_content.encode(), compresslevel=9)
base64_encoded = base64.b64encode(byte_object)

print(f"https://swissmodel.expasy.org/repository/uniprot/{protein_name['F']}?annot={base64_encoded.decode()}")
