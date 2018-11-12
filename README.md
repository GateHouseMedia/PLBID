# PLBID

We used the CDC's [Natality and Period Linked Birth-Infant Death Data Files](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm) to determine whether there was a difference in neonatal mortality rates and [five-minute Apgar scores of 0](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2943160/) among babies born in the hospital and those born outside the hospital from 2006-2015.

Specifically, we looked at four groups:
* babies born in a hospital with a midwife
* babies born in a hospital with a physician
* babies born at home with a midwife
* babies born in a freestanding birth center (not attached to a hospital) with a midwife

We restricted our analysis to full-term infants (37+ weeks gestation, weighing at least 2,500 grams) with no congenital anomolies or chromosomal disorders. In other words, we exluded babies who might have died or had an Apgar score of 0 regardless of birth setting or birth attendant. We also excluded twins and other multiple births. And we exluded babies born to mothers who were not U.S. residents and whose prenatal care might have happened outside of the United States.

We based our research on older studies done by [Amos Grunenbaum et al](https://www.documentcloud.org/documents/5030472-Grunenbaum-et-al-Papers.html) published in the American Journal of Obstetrics & Gynecology.

You can run a simpler analysis in [CDC WONDER](https://wonder.cdc.gov/lbd.html), but it does not allow you to break down the out-of-hospital births by specific location (home birth versus birth center birth). 

## Getting Started

### Download the PLBID flatfiles
You need to get both the CDC's [Birth Data flatfiles and Period Linked Birth-Infant Death Data flatfiles](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm) for every year beginning in 2006. 

If you have statistical software like SAS/SPSS/STATA, you can download the [code files here](http://www.nber.org/data/vital-statistics-natality-data.html). 

### Convert the flatfiles into a query-able format
Since we didn't have statistical software, we relied on the record layout in the User's Guide provided for each year to map out the fields based on character width. The record layout changes from time to time, so you have to pay attention across each year. For example: From 2006-2013, field containing the year of infant death was called **DTHYR** and located in character positions *1188-1191*. But from 2014-2015, the field changed its name to **DOD_YY** and its character positions to *1672-1675*.

We noted all the field names and character positions for each year in an Excel spreadsheet called **PLBID Fields 2006-2016.xlsx**, which is in our repository. The names and character positions are the same in the Birth Data files, but they don't include the fields related to the infant's death, obviously.

DAK FILLS IN THE PYTHON PART HERE ...

### Load the data into Google BigQuery
Or whatever database you prefer. But we used Google BigQuery because of the size of the files -- in particular, the Birth Data file (AKA, the numerator). 

### Query the data
Here are the queries I used to run the analysis.

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
AND LBO_REC = "1"
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
AND LBO_REC = "1"
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
AND LBO_REC = "1"
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
AND LBO_REC = "1"
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
AND LBO_REC = "1"
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
AND LBO_REC = "1"
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
AND LBO_REC = "1"
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
AND LBO_REC = "1"
AND (ATTEND = "3" OR ATTEND = "4")
AND CAST(AGER5 AS INTEGER) <4
```
