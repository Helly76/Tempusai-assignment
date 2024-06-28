# -*- coding: utf-8 -*-
"""TempusAI_assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P8a-TmV3UWNntm9qfqR2U6Jgy-Tur0pT
"""

import pandas as pd
import os
import glob
import requests
import sys


def get_user_input():
    #get the valid input from user
    while True:
        user_input = input("Please enter full path of input file: ")
        if user_input.strip() and os.path.isfile(user_input): 
            return user_input
        else:
            print("Input is not a valid file path. Please try again.")
            
print("TempusAI assignment varient annotation")
# define input and output path
input_path = get_user_input()
print("You entered input file path: ", input_path)
# Create an output file path based on the input
dir_path = os.path.dirname(input_path)
output_path = os.path.join(dir_path, 'Output_annotation.tsv')
print("You will get the output file at this location: ", output_path)
try:
    # Read the VCF file into pandas dataFrame, using comment to exclude information lines from the vcf file
    vcf_df = pd.read_csv(input_path,comment = '#' ,sep ='\t', header=None)

    # Include names as listed in VCF file
    vcf_df.columns =['CHROM',	'POS',	'ID',	'REF'	,'ALT',	'QUAL'	,'FILTER'	,'INFO'	,'FORMAT'	,'sample']

except Exception as e:
    print(f"An error occurred while reading the input file {input_path}, error: {e}")


# Extract Depth of sequence coverage at the site of variation from INFO, as per the definition provided in the vcf file
vcf_df['DP'] = vcf_df['INFO'].str.extract(r'QD=(\d+)').astype(float)

# Extract Number of reads supporting the variant from INFO, as per the definition provided in the vcf file
vcf_df['Total Reads'] = vcf_df['INFO'].str.extract(r'TR=(\d+)').astype(float)

# This is an additional column extracted to compute the perecntage in later step.
vcf_df['Forward read'] = vcf_df['INFO'].str.extract(r'NF=(\d+)').astype(float)

# compute Percentage of reads supporting the variant versus those supporting reference reads, as per the definition provided in the vcf file
vcf_df['percentage supporting reads'] = round((((( vcf_df['Total Reads']- vcf_df["Forward read"]))/vcf_df['Total Reads']) * 100),2)

vcf_df.head()

# Function to fetch variant information
def fetch_variant_info(row):
     # define the server and hgvs notations for API call
    server = "https://grch37.rest.ensembl.org"
    hgvs_notation = f"{row['CHROM']}:g.{row['POS']}{row['REF']}>{row['ALT']}"
    ext = "/vep/human/hgvs/"+hgvs_notation
    # adding parameters to get back variant class and all other required annotation information
    params = {
        "species": "homo_sapiens",
        "assembly": "GRCh37",
        "variant_set": "default",
        "format": "json",
        "variant_class": "1",
        "hgvs": "1",
        "content-type": "application/json",
    }

   # below is get api calls and parse the json ouput to get appropriate required annotation and if there are any error feteching than return N/A
    try:
        response = requests.get(server+ext, headers={ "Content-Type" : "application/json"}, json=params)
        response.raise_for_status()
        decoded = response.json()[0]  # Assuming only one variant per request
        variant_effect = decoded.get("most_severe_consequence", "N/A")
        gene = decoded.get("transcript_consequences", [{}])[0].get("gene_symbol", "N/A")
        gene_id = decoded.get("transcript_consequences", [{}])[0].get("gene_id", "N/A")
        variant_impact = decoded.get("transcript_consequences", [{}])[0].get("impact", "N/A")
        variant_consequence = decoded.get("transcript_consequences", [{}])[0].get("consequence_terms", "N/A")
        variant_class = decoded.get("variant_class", "N/A")
        minor_allele_freq = decoded.get("colocated_variants", [{}])[0].get("frequencies", {}).get(row['ALT'], {}).get("af", "N/A")
        clinical_significance = decoded.get("colocated_variants", [{}])[0].get("clin_sig", "N/A")
        clinical_significance_allele = decoded.get("colocated_variants", [{}])[0].get("clin_sig_allele", "N/A")
        phenotype = decoded.get("colocated_variants", [{}])[0].get("phenotype_or_disease", "N/A")
        # here inluded additional annotation like clinical significance and clinical allele as well as phenotype to get more insigits of the variant allele and associate with any known disease before
        # print(f"result found: {variant_effect},{gene},{gene_id},{variant_impact}, {variant_consequence}, {variant_class}, {minor_allele_freq},{clinical_significance}, {clinical_significance_allele}, {phenotype}")
        return variant_effect, gene, gene_id, variant_impact, variant_consequence, variant_class, minor_allele_freq, clinical_significance, clinical_significance_allele, phenotype

    except requests.RequestException as e:
        print(f"Error while fetching data for {hgvs_notation}: {e}")
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# Apply the function to each row in the DataFrame
vcf_df[["variant_effect", "gene", "gene_id", "variant_impact", "variant_consequence",
              "variant_class", "minor_allele_freq", "clinical_significance",
              "clinical_significance_allele", "phenotype"]] = vcf_df.apply(fetch_variant_info, axis=1, result_type="expand")

# Now variants_df contains the additional columns
final_columns = ["CHROM", "POS", "REF", "ALT","DP","Total Reads","Forward read", "percentage supporting reads",
                 "gene", "gene_id", "variant_effect", "variant_consequence",
                 "variant_class","variant_impact", "minor_allele_freq", "clinical_significance",
                 "clinical_significance_allele", "phenotype"]
final_df = vcf_df[final_columns]
print(vcf_df)

final_df.tail()

# saving annotation ouput as tsv file
final_df.to_csv(output_path, sep="\t")