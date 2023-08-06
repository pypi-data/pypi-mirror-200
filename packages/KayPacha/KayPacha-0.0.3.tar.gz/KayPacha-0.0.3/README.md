[![Python package](https://github.com/colav/KayPacha/actions/workflows/python-package.yml/badge.svg)](https://github.com/colav/KayPacha/actions/workflows/python-package.yml)

<center><img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/></center>

# KayPacha
SQL data extraction for Scienti and Colav parners  Oracle databases

# Description
Package extract the data from SQL databases from Oracle Databases from Scienti or Colav parners
Models are defined here, filters etc..

# Dependecies needed before installation
Before installing the package, you need to install Graphviz

## Ubuntu and Debian
`sudo apt-get install graphviz graphviz-dev`

If you need more information about the installation, visit: https://pygraphviz.github.io/documentation/stable/install.html

# Installation

## Package
`pip install kaypacha`


# Usage

## Scienti
Oracle DB Colav docker database for scienti have to be already loaded, [take a look here](https://github.com/colav/oracle-docker)

Remember you only can use max 2 threads due a Oracle XE version limitation [more information here](https://docs.oracle.com/en/database/oracle/oracle-database/18/xeinl/licensing-restrictions.html)

Saving the model product for scienti on MongoDB (default users are UDEA_CV,UDEA_GR,UDEA_IN)

`
kaypacha_scienti --mongo_dbname  scienti_udea_2022 --model product  --max_threads 2 --checkpoint
`

Saving all models for scienti on MongoDB

`
kaypacha_scienti --mongo_dbname  scienti_udea_2022 --max_threads 2 --checkpoint
`

Getting a JSon file sample for the model product for scienti (**WARNING**: getting the full DB in a file require a huge amount of RAM, use it with careful.)
`
kaypacha_scienti --mongo_dbname  scienti_udea_2022 --model product --json prod.json --max_threads 2 --sample
`

### Example university of externado

`
kaypacha_scienti --mongo_dbname  scienti_uec_2022 --model product --max_threads 2 --cvlac_user UEC_CV --gruplac_user UEC_GR --institulac_user UEC_IN --checkpoint
`

or

`
kaypacha_scienti --mongo_dbname  scienti_uec_2022 --model endorsement --max_threads 2 --cvlac_user UEC_CV --gruplac_user UEC_GR --institulac_user UEC_IN --checkpoint
`

### Entities models supported fo Scienti
* product (EN_PRODCUTO)
* netowrk (EN_RED)
* project (EN_PROYECTO)
* event (EN_EVENTO)
* patent (EN_PATENTE)

### TODO
* implement all the main tables for Scienti.
  * resgiter "EN_REGISTRO"
  * industrial_secret "EN_SECRETO_INDUSTRIAL"
  * recognition "EN_RECONOCIMIENTO"
  * art_product "EN_PROD_ARTISTICA_DETALLE"

## SIIU
Oracle DB Colav docker database for siiu have to be already loaded, [take a look here](https://github.com/colav/oracle-docker)

Remember you only can use max 2 threads due a Oracle XE version limitation [more information here](https://docs.oracle.com/en/database/oracle/oracle-database/18/xeinl/licensing-restrictions.html)

Saving the model project for siiu on MongoDB

`
kaypacha_siiu --model project  --max_threads 2 --checkpoint
`

Saving all models for siiu on MongoDB

`
kaypacha_siiu --max_threads 2 --checkpoint
`
Getting a JSON file sample for the model product for scienti (**WARNING**: getting the full DB in a file require a huge amount of RAM, use it with careful.)

Getting the first 100 registers

`
kaypacha_siiu --model project --json project.json --max_threads 2 --sample
`

Getting a random sample, 5.5% of the total amount of registers

`
kaypacha_siiu --model project --json project.json --max_threads 2 --rand_sample --sample_percent 5.5
`

Making a graph of the model (There are two types of files supported: svg and png)
`
kaypacha_siiu --make_diagram project svg
`

### Entities models supported fo SIIU
* project (SIIU_PROYECTO)


#### Some errors
`
[WARNING] ORA-12504: TNS:listener was not given the SERVICE_NAME in CONNECT_DATA
`
A possible solution is to use --ora_dburi 0.0.0.0:1521/XE


# Generating Diagrams with BlockDiag
Exaple for patent on scienti.<br>
Also support formats such as SVG and PDF.

`
kaypacha_blockdiag --model scienti --submodel patent --filename patent.png 
`
# License
BSD-3-Clause License 

# Links
http://colav.udea.edu.co/



