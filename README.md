# Tempus AI Technical challenge
TempusAI assignment varient annotation

Project Title and overview 
Tempus Bioinformatics Technical Challenge - variant annotation tool 
The variant annotation tool is created to solve the technical challenge provided by Tempus AI, and I am happy to share insights on my approach to solve this challenge. The variant annotation tool is a python tool which enables users to annotate variant alleles in the VCF file with the help of API calls from the ensembl-vep. It provides essential information about each variant, including depth of sequence coverage at site of variation, read support, variant type, gene details, minor allele frequency, and additional annotations include variant consequences, clinical_significance of allele.
For further details about how Ensembl predicts the effects of each allele I referred to the documentation of defined terms according to SO (Sequence ontology) which can be found here https://useast.ensembl.org/info/genome/variation/prediction/predicted_data.html
There is also detailed documentation on variant classification, which essentially dictates the type of variant based on the allele. Link to document here. https://useast.ensembl.org/info/genome/variation/prediction/predicted_data.html
These documentation are key to this challenge as it guided me to appropriate endpoints and parameters to be used for the API calls for accessing vep hgv notation. https://rest.ensembl.org/documentation/info/vep_hgvs_get 


**NOTE: The API calls from rest ensembl vep for annotating alleles in the vcf file provided for this challenge were performed on the species homo sapiens and genome assembly GRCh37 version. 


Required packates to install before run

pip install pandas
pip install requests

How to run the Project?

python3 tempusai_assignment.py 

(user will see this message to enter the input file path)
You entered input file path: /your/input/file/location/test_vcf_data.txt 

Usage 


* Must provide an input VCF file containing variants, ( test_vcf_data.txt) for this challenge.
* The program will annotate each variant and create an output VCF file (Output_annotation.tsv).


The script will require an input filepath (aka path to the file where you stored your vcf file) 




Features
1. Depth of Sequence Coverage at the site of variation
   * Gets the depth of sequence coverage at the variant site from input VCF file.


2. Percentage Supporting Reads:
   * Calculates the percentage of reads supporting the variant versus reference reads.
3. VEP Annotations:
   * Utilizes the VEP hgvs API to retrieve gene information, variant type, and effect.
VEP API Documentation (https://rest.ensembl.org/#VEP)
4. Minor Allele Frequency:
   * Retrieves the minor allele frequency from the VEP hgvs.
5. Additional Annotations:
   * Includes Clinical Significance, Clinical significance allele, Phenotype and variant consequence (which are some additional annotation to provide insights on variant allele and associated with other known disease and able to compare.




Output 
The default output format is a tab-delimited file, which reports all fields mentioned in the feature section above.
Output filename is set to default as Output_annotation.tsv and would be saved to the folder based on the user input filepath




Credit 
Thank you to Tempus for sharing such an exciting challenge.
