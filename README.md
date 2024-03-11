Our in-house Django-based tool to register genetic samples and make automatic conclusions for genetic reports. Currently only admin interface is used.


# Installation
- clone the repository: `git clone git@github.com:babinyurii/lab_genetic_reporter.git`
- run migrations: `python manage.py makemigrations`, `python manage.py migrate`
- run tests: `python manage.py test`
- run the project: `python manage.py runserver` or adapt the `run.bat` file for your project location

# Workflow

# Preparation of SNP, detection kits and conlusion templates

## 1. create database of SNPs
- go to `Markers` app, `SNPs` section
- create `SNPs` which are used in your detection kits

## 2. create database of detection kits 
- go to `DETECTION_KITS`, `SNP detection kits` section
- create detection kits and link `SNPs` which are used in your kits


## 3. create report rules
Report rule links any two SNPs together (which is the simplest haplotype) in any kit.
Report rule consists of 9 genotype combinations which have clinical significance for final report
- go to `SNP SAMPLES AND RESULTS` app, `1. Report rules for two SNP` section
- create report rule: choose two SNPs and link the rule to one or more detection kits

**When report rule is created, its 9 genotype combinations are generated in the section `2. report rules: conclusions for genotype combinations`**

## 4. fill in the conclusion text associated with each genotype combination
- go to `SNP SAMPLES AND RESULTS`, section `2. report rules: conclusions for genotype combinations`
- click each of the report rule and fill in the `report` section


# Working with samples

## 1. add sample
- go to `SNP SAMPLES AND RESULTS`, section `3. Samples`
- add sample and choose the detection kit which is used for research

**When sample is saved, the template for its results is generated in the section `4. SNP results`**

## 2. fill in the results after research
- go to `SNP SAMPLES AND RESULTS`, section `4. SNP results`
- fill in the genotype results for each result record

**When the last result for a particular sample is saved, the conlusion based on the report rule genotype combinations is generated in the `SNP SAMPLES AND RESULTS`, section `5. Conclusions for reports`**








