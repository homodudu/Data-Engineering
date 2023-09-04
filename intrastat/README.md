
# Intrastat

## Overview:
Intrastat is a system that collects information relating to the trade of goods. This project will transform sample invoice data from a fictitious company into a submittable Swedish intrastat declaration.

![alt text](https://github.com/homodudu/Data-Engineering/blob/main/intrastat/_resources/Process%20Flow%20V2.png)

## Aim:
Write a production ready data engineering pipeline using python and pandas.

## Task:
Below outlines the steps to be performed:

 01) Import the necessary libraries for the project.
 02) Define the functions that will facilitate the data engineering.
 03) Request intrastat commodity code list URL and read content into pd data frame.
 04) Request ECB FX rates from URL, parse xml file and read data into pd data frame.
 05) Cleanse and transform ex.rate data into pivot table.
 06) Request the sample intrastat data url and read content into pd data frame.
 07) Verify sample data using commodity code list.
 08) Apply daily exchange rate calculation on sample invoice values.
 09) Apply final transformations to intrastat output file.
 10) Display the content of the prepared file.
 11) Export the content as an excel file, submittable to the Swedish stats authority.

## Author:
- [@homodudu](https://www.github.com/homodudu)
