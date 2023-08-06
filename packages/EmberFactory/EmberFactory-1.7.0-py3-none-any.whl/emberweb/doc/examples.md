This page illustrates specific examples. As these are relatively elaborated, we suggest that you read the 
[Tutorial](tutorial) before adapting them to your needs. To understand the layout details, 
see the [Parameters reference](parameters).
In each example, the "download" button provides the corresponding input .xlsx file.

### SR15 and AR5 Reasons for concern

![AR5-SR15-RFCs](examples/images/AR5-SR15-RFCs.png#example "AR5-SR15-RFCs")

**Data**: Adapted from [10.5281/zenodo.3992857](https://doi.org/10.5281/zenodo.3992857), itself based on information
from the IPCC reports. <br>
Note:  As SR1.5 only evaluates risks up to 2.5°C, the upper limit of validity is changed in between the data tables. 

**Layout**: This example shows axis tick marks and minor tick marks (every 0.5°C = 2 minor ticks 
by major tick mark) with grid lines only for user-defined levels.

Note: here the embers are in the same order in the table and on the figure. 
When a figure needs to have a different order than the related table, even with a different
grouping of embers into "panels", it can be done without changing the data table,
hence without risk of errors. It is explained on the page describing [parameters](parameters#sorting).

[AR5-SR15-RFCs example](examples/AR5-SR15-RFCs.xlsx#example)

---
### AR5 Synthesis Report ocean acidification embers

![AR5-SYR-CO2](examples/images/AR5-SYR-CO2.png#example "AR5-SYR-CO2")

**Data**: This example is a partial reproduction of IPCC AR5 Synthesis Report (SYR) topic 2 figure 5.2, limited to 
the embers in the central panel.
The data is based on the analysis of the colours in the published figure (in the same way as the previous example). 
However, the original version contains tiny details, almost invisible, which are not reproduced here. 
Therefore, if you want to use this data,
please e-mail us.

**Layout**: This example shows a case without vertical axis line (as in the original), with an "hazard" scale other
than global mean temperature increase (CO<sub>2</sub> concentration)

[AR5-SYR-CO2 example](examples/AR5-SYR-CO2.xlsx#example)

---
### Special report on Ocean and cryosphere (SROCC)

![SROCC_SPM3](examples/images/SROCC_SPM3.png "SROCC_SPM")

[SROCC_SPM3 example](examples/SROCC_SPM3.xlsx)

**Data**: Table SM 5.6b and SM 5.8b from the SROCC, retaining only the embers in SROCC Fig SPM.3 panel d.
For the original version, see [ErrataFigureSPM3d.png](https://www.ipcc.ch/site/assets/uploads/sites/3/2020/11/SROCC_SPM_ErrataFigureSPM3d.png)
from ipcc.ch. 

**Layout**:
The layout is quite close to the original, showing a range of temperatures as grey background ('present
day' = 2006-2015, with a 'label offset' defined in the Excel file to move that text down and thus avoid overlapping
the axis data).