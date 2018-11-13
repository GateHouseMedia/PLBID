# PLBID

We used the CDC's [Natality and Period Linked Birth-Infant Death Data Files](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm) to determine whether there was a difference in neonatal mortality rates and [five-minute Apgar scores of 0](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2943160/) among babies born in the hospital and those born outside the hospital from 2006-2015.

Specifically, we looked at four groups:
* babies born in a hospital with a midwife
* babies born in a hospital with a physician
* babies born at home with a midwife
* babies born in a freestanding birth center (not attached to a hospital) with a midwife

For the neonatal mortality analysis, we restricted our analysis to full-term infants (37+ weeks gestation, weighing at least 2,500 grams) with no congenital anomolies or chromosomal disorders. In other words, we exluded babies who might have died regardless of birth setting or birth attendant. We also excluded twins and other multiple births. And we exluded babies born to mothers who were not U.S. residents and whose prenatal care might have happened outside of the United States.

For the Apgar=0 analysis, we we restricted our analysis to full-term infants (37+ weeks gestation, weighing at least 2,500 grams) who were not twins or triplets, etc. But we did not exlude babies who had congenital anomolies or chromosomal disorders, nor did we exclude babies of non-U.S. resident mothers.

We based our research on older studies done by [Amos Grunenbaum et al](https://www.documentcloud.org/documents/5030472-Grunenbaum-et-al-Papers.html) published in the American Journal of Obstetrics & Gynecology.

You can run a simpler analysis in the user-friendly [CDC WONDER](https://wonder.cdc.gov/lbd.html) online database, but it does not allow you to break down the out-of-hospital births by specific location (home birth versus birth center birth). It's still a nice feature, though, and I would recommend it if you want to bypass converting flatfiles.

## Getting Started

### Download the PLBID flatfiles
You need to get both the CDC's [Birth Data flatfiles and Period Linked Birth-Infant Death Data flatfiles](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm) for every year beginning in 2006. 

If you have statistical software like SAS/SPSS/STATA, you can download the [code files here](http://www.nber.org/data/vital-statistics-natality-data.html). 

### Convert the flatfiles into a query-able format
Since we didn't have statistical software, we relied on the record layout in the User's Guide provided for each year to map out the fields based on character width. The record layout changes from time to time, so you have to pay attention across each year. For example: From 2006-2013, the field containing the year of infant death was called **DTHYR** and located in character positions *1188-1191*. But from 2014-2015, the field changed its name to **DOD_YY** and its character positions to *1672-1675*.

We noted all the field names and character positions for each year in an Excel spreadsheet called **PLBID Fields 2006-2016.xlsx**, which is in our repository. The names and character positions are the same in the Birth Data files, but they don't include the fields related to the infant's death, obviously.

We then used a Python script to combine the data across all the years into one big data set with the appropriate fields for us to query. 

### Prerequisites
Python ( 2.7 or greater ).  
Pandas module - `pip install pandas `  
If you are using Python 2.7 the xlrd module may also be needed - ` pip install xlrd `  

### Running the script
From the command line or terminal execute the ```parseCDC.py``` Python script and provide the required parameters.  
  `-i <input file name>` ( the CDC file to parse )  
  `-s <sheet name>` ( name of the Excel sheet to grab column positions from )
  
Example command for VS13LINK.PSNUMPUB ( found in the example folder ). Since the column positions for 2013 are on the 2011-2013 sheet we will pass that to -s parameter  
```python parseCDC.py -i 'example/VS13LINK.PSNUMPUB' -s '2011-13'```

This will create a new CSV file in the same folder as the input file. 

### Load the data into Google BigQuery
Or whatever database you prefer. But we used Google BigQuery because of the size of the files -- in particular, the Birth Data file (AKA, the numerator), which contains tens of millions of records. 

### Query the data
Here are the queries we used to run the analysis. Note that you will have to pull birth data from the Birth Data file (denominator) and death data from the PLBID file (numerator).

#### Early neonatal mortality (infant death within 0-6 days of birth)

Infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "1" OR ATTEND = "2")
```
Deaths of infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "1" OR ATTEND = "2")
AND CAST(AGER5 AS INTEGER) <4
```

Infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "3" OR ATTEND = "4")
AND CAST(AGER5 AS INTEGER) <4
```

Infants delivered by freestanding birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "2" OR BFACIL = "2")
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by freestanding birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "2" OR BFACIL = "2")
AND (ATTEND = "3" OR ATTEND = "4")
AND CAST(AGER5 AS INTEGER) <4
```
Infants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "4" OR BFACIL = "3" OR OR BFACIL = "4" OR OR BFACIL = "5")
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "4" OR BFACIL = "3" OR OR BFACIL = "4" OR OR BFACIL = "5")
AND (ATTEND = "3" OR ATTEND = "4")
AND CAST(AGER5 AS INTEGER) <4
```
#### Early neonatal mortality of FIRST CHILD (infant death within 0-6 days of birth)

Infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND TBO_REC = "1"
AND (ATTEND = "1" OR ATTEND = "2")
```

Deaths of infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND TBO_REC = "1"
AND (ATTEND = "1" OR ATTEND = "2")
AND CAST(AGER5 AS INTEGER) <4
```

Infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
AND CAST(AGER5 AS INTEGER) <4
```

Infants delivered by freestanding birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "2" OR BFACIL = "2")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by freestanding birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "2" OR BFACIL = "2")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
AND CAST(AGER5 AS INTEGER) <4
```

Infants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "5")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
```

Infants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "5")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
AND CAST(AGER5 AS INTEGER) <4
```

#### Neonatal mortality (infant death within 0-27 days of birth)

Infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "1" OR ATTEND = "2")
```

Deaths of infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "1" OR ATTEND = "2")
AND AGER5 != "5"
```

Infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "3" OR ATTEND = "4")
AND AGER5 != "5"
```

Infants delivered by freestanding birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "2" OR BFACIL = "2")
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by freestanding birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "2" OR BFACIL = "2")
AND (ATTEND = "3" OR ATTEND = "4")
AND AGER5 != "5"
```

Infants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "4")
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of fnfants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "4")
AND (ATTEND = "3" OR ATTEND = "4")
AND AGER5 != "5"
```

#### Neonatal mortality of FIRST CHILD (infant death within 0-27 days of birth)

Infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND TBO_REC = "1"
AND (ATTEND = "1" OR ATTEND = "2")
```

Deaths of infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND TBO_REC = "1"
AND (ATTEND = "1" OR ATTEND = "2")
AND AGER5 != "5"
```

Infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "1" OR BFACIL = "1")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
AND AGER5 != "5"
```

Infants delivered by freestandingn birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "2" OR BFACIL = "2")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by freestandingn birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "2" OR BFACIL = "2")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
AND AGER5 != "5"
```

Infants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "5")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
```

Deaths of infants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.NUM]
WHERE BWTR4 = "3"
AND RESTATUS != "4"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (CA_ANEN != "Y" OR UCA_ANEN != "1")
AND (CA_MNSB != "Y" OR UCA_SPINA != "1")
AND CA_CCHD != "Y"
AND (CA_CDH != "Y" OR UCA_HERN != "1")
AND (CA_OMPH != "Y" OR UCA_OMPH != "1")
AND CA_GAST != "Y"
AND CA_LIMB != "Y"
AND (CA_CLEFT != "Y" OR UCA_CLIP != "1")
AND CA_CLPAL != "Y"
AND CA_HYPO != "Y"
AND (CA_DISOR = "N" OR CA_DISOR = "U")
AND (CA_DOWN = "U" OR CA_DOWN = "N" OR UCA_DOWN != "1")
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "5")
AND TBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
AND AGER5 != "5"
```

#### Apgar Score of 0

Infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "1" OR ATTEND = "2")
```

Infants delivered by hospital physicians with Apgar=0
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "1" OR ATTEND = "2")
AND APGAR5 = “00"
```

Infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "3" OR ATTEND = "4")
```

Infants delivered by hospital midwives with Apgar=0
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "3" OR ATTEND = "4")
AND APGAR5 = “00"
```

Infants delivered by freestanding birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (UBFACIL = "2" OR BFACIL = "2")
AND (ATTEND = "3" OR ATTEND = "4")
```

Infants delivered by freestanding birth center midwives with Apgar=0
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (UBFACIL = "2" OR BFACIL = "2")
AND (ATTEND = "3" OR ATTEND = "4")
AND APGAR5 = “00"
```

Infants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "5")
AND (ATTEND = "3" OR ATTEND = "4")
```

Infants delivered by home midwives with Apgar=0
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "5")
AND (ATTEND = "3" OR ATTEND = "4")
AND APGAR5 = “00"
```

#### Apgar Score of 0 for FIRST CHILD

Infants delivered by hospital physicians
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND TBO_REC = "1"
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "1" OR ATTEND = "2")
```

Infants delivered by hospital physicians with Apgar=0
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND TBO_REC = "1"
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "1" OR ATTEND = "2")
AND APGAR5 = “00"
```

Infants delivered by hospital midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND TBO_REC = "1"
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "3" OR ATTEND = "4")
```

Infants delivered by hospital midwives with Apgar=0
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND TBO_REC = "1"
AND (UBFACIL = "1" OR BFACIL = "1")
AND (ATTEND = "3" OR ATTEND = "4")
AND APGAR5 = “00"
```

Infants delivered by freestanding birth center midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND TBO_REC = "1"
AND (UBFACIL = "2" OR BFACIL = "2")
AND (ATTEND = "3" OR ATTEND = "4")
```

Infants delivered by freestanding birth center midwives with Apgar=0
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND TBO_REC = "1"
AND (UBFACIL = "2" OR BFACIL = "2")
AND (ATTEND = "3" OR ATTEND = "4")
AND APGAR5 = “00"
```

Infants delivered by home midwives
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND TBO_REC = "1"
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "5")
AND (ATTEND = "3" OR ATTEND = "4")
```

Infants delivered by home midwives with Apgar=0
```
SELECT COUNT (*) FROM [iteam-156720:BID.DEN]
WHERE BWTR4 = "3"
AND GESTREC3 = "2"
AND DPLURAL = "1"
AND TBO_REC = "1"
AND (UBFACIL = "4" OR BFACIL = "3" OR BFACIL = "4" OR BFACIL = "5")
AND (ATTEND = "3" OR ATTEND = "4")
AND APGAR5 = “00"
```
