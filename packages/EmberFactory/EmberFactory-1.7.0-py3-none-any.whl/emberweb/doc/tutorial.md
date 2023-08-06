This page is the starting point to learn about the preparation of data for the 'Ember Factory'. 
It provide  examples of input files with increasing flexibility.

To make 'ember' diagrams from your own data, start from the Standard input file format below, 
which contains a standard IPCC-style data table
(note that no files are 'from the IPCC' or under its responsibility: see [more information](../more)).

Section 1 below should cover most needs when you begin. If you face difficulties such overlapping text in
your diagram, continue to section 2 about the layout parameters. Those parameters also allow for selecting and
sorting embers from your data before plotting, or adding some types of information on the diagram. 
For more details about the parameters, see [Parameters](parameters).

# Standard input file format 

This format (previously called "Basic") is based on tables provided in the supplementary material 
of IPCC Special reports published in 2019. The files indicate the level of global warming (or other 'hazard metric') 
which corresponds to "risk transitions", i.e. changes from one risk level to the next, 
according to a standard scale of risk used by the IPCC in several of its reports.

Files contain a main spreadsheet containing the ember data and optional metadata. 
Additional spreadsheets are optional and makes it possible to fine-tune the presentation of the embers diagram, 
as explained in the next sections. The main spreadsheet contains the following information:

* **global metadata**, such as project name, data source, revision date, and a limited set of
  parameters controlling how the data will be shown (as parameter name - value in columns A and B)
* **ember group names**: an optional name for a set of embers (it must be provided in column A and
  will be shown on top of the group of embers on the diagram);
* **ember data tables**: _the key information from the risk assessment_, used to draw the 'burning embers'. 
  _It must be organised as shown in the examples_, and you may copy-paste as many 'embers' data tables as you need.
  _An ember has a name in column B and includes its data in several rows until there is a blank line or
  other ember name_ (see examples). Embers always start in _column B_. See "ember data tables" below for details

## Example

[SRCCL figure SPM.2B](examples/Basic-fmt-SRCCL.xlsx)

This example contains the data from table SM7.6 of the Special Report on Climate change and Land. 
The resulting 'burning ember diagram' appears in the Summary for Policymakers as 
[figure 2, panel B (IPCC website)](https://www.ipcc.ch/site/assets/uploads/2019/08/SPM2-approval-FINAL-1.pdf).

## Template for new embers

[Standard template](examples/Basic-template.xlsx)

This spreadsheet does not contain real data, but rather generic names intended to help identifying how it can be 
modified. 

## Details about the tables describing each ember

The (part of) table describing each ember (in the spreadsheet) describes the transitions between risk levels, 
following the format used in the report of the IPCC AR6 cycle. An example is,

| &nbsp;  | Name                               | Risk transition          | &nbsp; | Hazard level | Confidence |
|---------|------------------------------------|--------------------------|--------|--------------|------------|
|         | RFC1 Unique and threatened systems | Undetectable to moderate | Min    | 0.4          | Very high  |
|         | &nbsp;                             | &nbsp;                   | Median | 0.5          | &nbsp;     |
|         | &nbsp;                             | &nbsp;                   | Max    | 0.7          | &nbsp;     |
| (empty  | &nbsp;                             | Moderate to high         | Min    | 0.7          | Very high  |
| column) | &nbsp;                             | &nbsp;                   | Median | 0.9          | ...        |

The "Median" (midpoints) are *optional* : a given ember may combine transitions with or without midpoints.

For very specific cases, "percentiles" (introduced in version 1.7) may specify the hazard level corresponding
to other levels of risk within the transition. Here percentiles simply mean X/100 of the color change within a
transition. For example, one my write "p50" instead of "median" (the general form is pX). 
It is possible to specify several percentiles, e.g. replace the median with 2 lines for p33 and p66, providing 
corresponding hazard levels. This was introduced with the expectation that it will rarely be used, because
it requires the assessment of details beyond what is generally available and needed to represent transitions.

## General parameters provided in the "data" spreadsheet

A few parameters, mainly related to the data itself, can be set in the same spreadsheet as the data. 
The most common ones are the following:

|||
|--------------------|---------------------------------------------------------|
|haz_axis_top        | The top value in the hazard axis |
|haz_name            | Name of the hazard variable (such as 'Global mean temperature'), used as axis name |                                                         |
|haz_unit            | Unit of the hazard variable (added to the axis labels, except if already included in haz_name)|

None of these parameters is mandatory: there are default values, for more information on the 
metadata and other parameters, see [Parameters](parameters). 

# Optional 'Graph parameters' sheet

The simple files described in the previous section only provide access to a few parameters.
They are sufficient to reproduce most types or 'burning ember' figures published so far, 
but with limitations regarding layout details.
To avoid cluttering the sheet that contains the assessment data, we provide layout-related parameters in an additional
sheet, which must be named "Graph parameters".

If you started from a file presented in section 1, it is easy to add the layout parameters
in your existing Excel file: download the example from this section and copy the "Graph parameters"
spreadsheet in your existing file (in Excel, start from the downloaded example and right-click on the tab
showing the Graph parameters spreadsheet). There is no need to include all parameters: a "Graph parameters" sheet
including just one parameter would have this parameter taken into account and all others kept to their default values.

[SRCCL example + layout](examples/Basic-layout-SRCCL.xlsx)

The "Basic+layout" example includes the additional 'layout' sheet with most (but not all) possible parameters.
This particular example illustrates the following:

- **horizontal grid lines** (in this example 0, 1, 2, 3 °C). The selection of these levels may (simultaneously) use two
definitions, provided in the parameter `haz_grid_lines`. The first value (here: 3) is a target number of levels which
the software may adapt slightly in order to provide 'nice' levels (here : the 4 values 0, 1, 2, 3). The next columns on
the right additionally provide absolute values of levels that have to be plotted (here: a line is added at 1.5°C).
For more information and more complex example, see [Parameters](parameters#gridlines)

- **legend position** (in this example `leg_pos = right`). The most common values are *under*, *right*, and *none*. 
For more information, see [Parameters](parameters#legpos)

- **confidence levels presentation**. These can be show in different ways: a number of dots was used in the most recent 
IPCC practice (see SROCC SPM.3), while letters (L for Low confidence, H for Medium, ...) where used in the SRCCL.  
The names of confidence levels (Low, Medium...) used in the data sheet are translated to symbols for the diagram 
according to a table which is at the bottom of the 'layout' sheet. 
You could fill anything as output (`conf_levels_graph`), so even translations could potentially be done in this way.

The resulting figure is significantly closer to the layout of the published figure 
([figure 2, panel B (IPCC website)](https://www.ipcc.ch/site/assets/uploads/2019/08/SPM2-approval-FINAL-1.pdf));
this shows the flexibility generated by using the 'Graph parameters' sheet.<a class="anchor" name="sort"></a>

There are other options illustrated in this Excel file, such as the possibility to **sort the embers**.
This makes it possible to generate different diagrams without changing the 'data' sheet, by listing ember names 
in the desired order. See [Parameters](parameters) for more information.<a class="anchor" name="Colour"></a>

# Colour Palettes and colour models

If you do not have specific colour needs, keep the standard/defaults settings. 
The EmberFactory supports arbitrary colour palettes for the ember gradients. There are two ways to change colours:

- by changing the parameter `be_palette`: see this parameter in [Parameters](parameters) to find the allowed names.

- by adding a spreadsheet named "Color definitions" [`Color`, not `Colour`].
Examples are provided here: [example Color definitions](examples/colors.xlsx). 
Copy the "Color definitions" sheet in your workbook, then  add your own colour palette starting from a 
copy of the cells which defines an existing one. The name of each colour palette is indicated by 
the parameter "PALETTE": please use a new name to avoid confusion with the default ones. When done, select your
palette in the Graph parameter sheet with `be_palette`.

Both RGB and CMYK colour palettes are available. However, if you use CMYK, beware that this will only be provided in
the PDF files, as this colour model is not supported in PNG or JPEG files. For more information on colour palettes,
please e-mail philippe.marbaix@uclouvain.be

# Adding ember-specific metadata

Starting with version 1.4 of the EmberFactory, there is some support for metadata about each ember.
This data is intended for future use (possibly outside the current user interface).
Ember metadata is provided as additional columns at the right of the ember data, 
as shown in [Example with ember metadata](examples/Basic-fmt-ember-metadata.xlsx).
Tentative metadata names are currently the following: 
*Remarks, Description, Keywords, Long name, Inclusion level, References*.
It is not mandatory to provide a complete set of metadata, but names outside this list will produce a warning.
For more information about future plans, please contact philippe.marbaix@uclouvain.be.

# Fullflex format (deprecated!)

The fullflex format was developed for Zommers et al. [1]. 
It initially provided more flexibility tha the 'standard' format found in tables of IPCC special report.
Due to developments, the standard format should be used for all new embers.
This version of the EmberFactory still supports the fullflex format for legacy reasons.

## Zommers et al. 2020<a class="anchor" name="Z2020"></a>

The data used in figure 3 of Zommers et al. [1] is available from 
[doi.org/10.5281/zenodo.4011178](https://doi.org/10.5281/zenodo.4011178);
The approach for obtaining this data is decribed in [Marbaix (2020)](https://doi.org/10.5281/zenodo.3992856).

Additionally, 
[RFCs-data-2020_01_26-Z2020_rev1_byPubli.xlsx](https://climrisk.org/RFCs-data-2020_01_26-Z2020_rev1_byPubli.xlsx) 
shows the embers sorted by publication (instead of by Reason for concern).
Both files contain the same data, while the different sorting is triggered by parameters in the 'layout' spreadsheet.

[1] Zommers, Z., Marbaix P, Fischlin A., Ibrahim Z. Z., Grant Z, Magnan A. K., Pörtner H-O, Howden M., Calvin K., 
Warner K., Thiery W., Sebesvari Z., Davin E. L., Evans J.P., Rosenzweig, C., O’Neill B. C., Anand Patwardhan, 
Warren R., van Aalst M. K. and Hulbert M. (2020).
*Burning Embers: Towards more transparent and robust climate change risk assessments*. 
Nature Reviews Earth & Environment. [doi.org/10/gg985p](https://doi.org/10/gg985p).<a class="anchor" name="failure"></a>

# It did not work! Why?

The Ember Factory is tested on several figures. However, it might be that you created an input file that includes
something that we missed. We make efforts to deal with a variety of cases that may produce a diagram as well as
with cases of "malformed inputs". If you received error messages, have a look at these: does it show that the 
processing ended at a specific point, such as while reading or drawing one of your embers? If the list of 
parameters is already visible (it is produced at the roughly the middle of the process), 
a quick look may show you that some are not set as you would expect. 

If you obtained a graphic, but it is not what you expected, you may click on "View / hide log information". This will
show a list of processing steps including the value of all parameters which were used and information about the 
colour gradients for each ember.

In any case, reporting errors or unsatisfying results helps improving the software! 
Please drop an e-mail to philippe.marbaix@uclouvain.be (a title such as "EmberFactory issue" may help).

# Further improvements & documentation

Comments are welcome. We will make our best to respond to requests regarding improvement,
documentation, or specific features, adapting the application if needed.
(see contact below).