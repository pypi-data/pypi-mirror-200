# -*- coding: utf-8 -*-
"""
makember produces a full burning ember plot from colour levels read from a table (.xlsx).

The objectives are to
- facilitate reproducibility of existing figures,
- facilitate the creation of new 'ember' figures in a way that is both quick and reliable.
This code is written in https://en.wikipedia.org/wiki/Python_(programming_language)
using the open-source library ReportLab from https://www.reportlab.com

Copyright (C) 2020  philippe.marbaix@uclouvain.be
"""
import numpy as np
import os
import warnings
from reportlab.lib import units
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT
from embermaker import helpers as hlp
from embermaker.helpers import norm
from embermaker import ember as emb
from embermaker import parameters as param
from embermaker.__init__ import __version__
trd = emb.Transition  # Transition definitions

# For an upcoming release (none of this appears urgent):
# Todo: Test the support for reading confidence levels in the "extended" format
#      (implemented but not fully tested with 'extended' format data sheets, but well tested with the basic format)

# Input file
# ----------
# This code can process 3 file formats:
# - The standard file format only contains data about the risk and confidence levels,
#   in the format from the IPCC SRCCL chap 7 supplementary material; the workbook only contains one sheet.
# - The extended file format contains the same first sheet, but one or two additional sheets provide:
#   . graphic parameters
#   . color definitions
# - The legacy "fullflex" format uses a different sheet to provide the data about the risk levels;
#   It was used for Zommers et. al (2020). The 'standard format' was made more flexible, so that this no longer needed.
#   Graphic parameters and colors are provided in the same way as in the "extended" file format above.


def makember(infile=None, outfile=None, prefcsys='CMYK'):
    """
    Reads ember data from .xlsx files, reads default values if needed, and generates an ember plot;
    in principle, this part of the plotting relates to the most 'high level' aspects that decides for the design,
    while lower level aspects are delegated to the ember module.
    :param infile: The name of the data file (.xlsx). Mandatory.
    :param outfile: An optional name for the output file; default = path and name of infile, extension replaced to .pdf
    :param prefcsys: The prefered color system (also called mode): RGB or CMYK.
    :return: a dict potentially containing : 'outfile' (output file path), 'width' (diagram width), 'error' (if any)
    """
    # Input file:
    if infile is None:
        return {'error': hlp.addlogfail("No input file.")}

    # Open input file (workbook):
    wbmain = hlp.secure_open_workbook(infile)

    # The file containing default values for parameters or colors will only be open if needed:
    def getwbdef():
        infdef = os.path.join(hlp.getpath_defaults(), "colors.xlsx")
        return hlp.secure_open_workbook(infdef)

    # Get graph parameters
    # --------------------
    gp = param.ParamDict()

    # Set Deprecated parameters:
    #               old name        ((tuple of new names)             , warning message)
    gp.setdeprecated({'haz_top_value': (('haz_axis_top', 'haz_valid_top'), None),
                      'haz_bottom_value': (('haz_axis_bottom', 'haz_valid_bottom'), None)})

    # Get parameter names, types, and default values:
    gp.readmdfile(os.path.join(hlp.getpath_defaults(), "paramdefs.md"))

    # Get user-specific parameters if provided
    # Todo: consider revising and moving this code to a dedicated section (11/2020)
    if "Graph parameters" in wbmain.sheetnames:
        sht = wbmain["Graph parameters"]
        for row in sht.rows:
            if isinstance(row[0].value, str):
                key = row[0].value.strip()
                # Find the position of the last non-empty cell + 1, or 1 if there is none:
                # (next just gets the first value of the iterator, which is what we want; the list is read from its end)
                rowlen = next(i for i in range(len(row), 0, -1) if row[i - 1].value or i == 1)
                # Main part of the parameteter : empty str will leave the default value untouched, '-' would delete:
                main = row[1].value
                isunit = rowlen > 2 and row[2].value in ['cm', 'mm']
                if isunit:
                    main *= getattr(units, row[2].value)
                if not hlp.isempty(main):
                    gp[key] = main
                # The user provided a list of values -> store this as list part of the parameter:
                if rowlen > 2 and not isunit:
                    gp[key] = [c.value for c in row[2:rowlen]]

    # Read the ember's data sheet
    # ---------------------------
    rembers = readembers(wbmain.worksheets[0], gp=gp)
    # Abort and pass error message if any. There is probably something more elegant, but it has yet to be designed :-).
    if 'error' in rembers:
        return rembers
    lbes = rembers['lbes']
    gp = rembers['gp']

    # Get colours palette
    # -------------------
    cpalname = None if 'be_palette' not in gp.keys() else gp['be_palette']
    # The UI color choice overrides any choice in the user file; if the UI asks for a default palette, use default wb
    if "Color definitions" not in wbmain.sheetnames or cpalname is None or prefcsys != "standard":
        hlp.addlogmes("Colours: will use default palettes.")
        wbcol = getwbdef()
    else:
        hlp.addlogmes("Colours: will use user-provided palettes.")
        wbcol = wbmain
    cpal = emb.getcpal(wbcol, prefcsys=prefcsys, cpalname=cpalname)

    # Log parameters
    # --------------
    hlp.addlogmes("Used parameters: " + str(gp))

    # Create the ouput file
    # ---------------------
    if outfile is None:   # Todo: have a look here - which method needs to handle files and canevas? <===============
        outfile = (os.path.splitext(infile)[0] + '.pdf').replace('/in/', '/out/')

    drawout = drawembers(lbes, gp, cpal, outfile)
    return drawout

# Todo: having egr out of the drawing function does not seem very practical... we don't have the colours... <======


def drawembers(lbes, gp, cpal, outfile):
    """
    Draws a figure containing embers
    :param lbes:
    :param gp:
    :param cpal:
    :param outfile:
    :return:
    """
    # Create the drawing canevas, and ember-diagram object
    # ----------------------------------------------------
    egr = emb.EmberGraph(outfile, cpal, gp)  # ember-diagram
    c = egr.c  # Drawing canvas

    # Optional mapping to a different hazard unit or hazard reference level
    # ---------------------------------------------------------------------
    # Todo: review this to check for logical consistency, hence long-term reliability.
    #       originally this was needed due to the storage of risk and hazard levels, but now
    #       the question is whether we need to change the level data *at this stage* or later in the drawing process.
    if gp['haz_map_factor'] is not None:
        hlp.addlogwarn("A scaling of the vertical (hazard) axis is requested in the input file (change in unit);"
                       " haz_map_factor= " + str(gp['haz_map_factor']))

        for be in lbes:
            for level in be.levels():
                level['hazl'] = level['hazl'] * gp['haz_map_factor']

    if gp['haz_map_shift'] is not None:
        hlp.addlogwarn("A change in the reference level for the vertical axis (hazard) was requested in the input file;"
                       " haz_map_shift= {}".format(gp['haz_map_shift']))
        for be in lbes:
            for level in be.levels():
                level['hazl'] = level['hazl'] + gp['haz_map_shift']

    # Sort the embers, if requested (option)
    # --------------------------------------
    # There are two sorting levels. The sorting needs to be done on the second criteria first.
    # Second sorting level
    if norm(gp['sort_2nd_by']) == 'name':
        sortlist = norm(gp.lst('sort_2nd_by'))
        # Standard Python sorting by f=skeyname + delete embers not in sortlist:
        lbes = emb.selecsort(lbes, emb.get_skeyname(sortlist))
        hlp.addlogmes(f"Secondary sorting by name; values: {sortlist}")
    if norm(gp['sort_2nd_by']) == 'group':
        sortlist = norm(gp.lst('sort_2nd_by'))
        lbes = emb.selecsort(lbes, emb.get_skeygroup(sortlist))
        hlp.addlogmes(f"Secondary sorting by group; values: {sortlist}")

    # The first level may swap the role of ember group and name: this allows grouping by names (becoming 'groups')
    if norm(gp['sort_first_by']) in ['name', 'group']:
        # Allow sorting according to an order set by a list in the Excel sheet:
        sortlist = norm(gp.lst('sort_first_by'))
        hlp.addlogmes(
            f"Primary sorting by: {gp['sort_first_by']}; values: {sortlist}")
        # Allow grouping by name instead of group, by swapping groups and names:
        if norm(gp['sort_first_by']) == 'name':
            for be in lbes:
                be.name, be.group = be.group, be.name
        # Sort
        lbes = emb.selecsort(lbes, emb.get_skeygroup(sortlist))

    # Generate group of embers (sublists) to prepare for drawing
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # index of embers which are not in the same group as the previous one
    ids = [i for i in range(1, len(lbes)) if lbes[i - 1].group != lbes[i].group]
    ids.insert(0, 0)  # add id=0 for first ember to build a list of index ranges defining groups
    ids.append(len(lbes))  # add  id+1 for the last ember (end of last range of embers)
    # List of groups of burning embers (nested list):
    glbes = [lbes[i:j] for i, j in zip(ids[0:len(ids) - 1], ids[1:])]

    # Draw the ember diagram
    # ----------------------
    # General notations:
    # x and y are coordinates on the canvas;
    # xbas, ybas define the bottom-left corner of the next element to be drawn
    # xbas first locates the left of the axis area, then the left of the ember group, then the left of each ember
    # be_ define lengths on the canvas read from the "gp" (graphic-) parameters found in a file.
    mxpos = 0  # The role of mxpos is to track the maximum width of the canvas on which something was drawn.
    # The following values are used to calculate the uppermost vertical position then draw towards the bottom
    gry = gp['be_bot_y'] + gp['be_y'] + gp['be_top_y']  # total height of the ember part
    if norm(gp['leg_pos']) == 'under':
        legy = gp['leg_bot_y'] + gp['leg_y'] + gp['leg_top_y']  # total height of the legend part
    else:
        legy = 0 * units.cm  # Legend is on the right: no need for vertical space
    # Embers are drawn in one or mutiple lines
    # The full figure does not have a fixed size: it is simply of the size needed to draw all the provided embers.
    # First define the number of graphic lines needed for the diagram:
    # (max_gr_line is the max number of embers per line, by default it is all the embers in one line)
    glines = np.ceil(len(glbes) / gp['max_gr_line'])

    # y-position of the first line of embers:
    ybas = ((glines - 1) * gry + legy + gp['be_bot_y'] + gp['be_y'] / 2.0)
    xbas = 0

    be_y = gp['be_y']
    be_x = gp['be_x']
    be_stp = be_x + gp['be_int_x']

    igrl = 0  # Number of groups in the current line
    il = 0  # Number of the current line

    # iterate over groups for drawing
    # - - - - - - - - - - - - - - - -
    for gbes in glbes:

        # Start a line of ember groups
        # - - - - - - - - - - - - - - -
        igrl += 1  # Move to next ember group in the current graphic line
        # If new graphic line, initialize relevant parameters:
        if igrl > gp['max_gr_line'] or il == 0:
            xbas = 0
            igrl = 1
            il += 1
            # Position of the bottom of the current BE draw area:
            ybas = (glines - il) * gry + legy + gp['be_bot_y']

        hlp.addlogmes('Drawing group: ' + str(gbes[0].group), mestype='title')

        # Y-coordinate (hazard levels) and axis
        # - - - - - - - - - - - - - - - - - - -
        # Pin the y coordinates to the drawing canvas for this group of embers (who will share the same y axis)
        # After this definition of the y-coordinates, egr will be used for any scaling to the canvas.
        # it is not possible to change the scaling (= how an hasard level is converted to canvas coordinate)
        # other than by calling 'pincoord'.
        # pincoord is called for each group of embers, never inside a group as it shares the same axis.
        egr.pincoord(ybas, be_y)

        # Draw the vertical axis and grid lines (using the y coordinates set by pincoord)
        # The axis name is shown only for the first ember of a line, and
        # vaxis returns the xbas value for the left of the 'ember area' = left of the grid lines
        xbas, xend = egr.vaxis(xbas, len(gbes), showname=(igrl == 1))

        # Group title
        xavlenght = len(gbes) * be_stp
        # Position in x starts at the left of the first ember colour bar (design choice) => add be_int_x/2
        hlp.drawparagraph(c, xbas + gp['be_int_x'] / 2.0, ybas + be_y + gp['be_top_y'] * 0.25, gbes[0].group,
                          length=xavlenght, font=("Helvetica", gp['gr_fnt_size']))

        bexs = []
        ahlevs = []

        # iterate over the embers in a group
        # - - - - - - - - - - - - - - - - - -
        for be in gbes:
            hlp.addlogmes('Drawing ember: ' + be.name, mestype='subtitle')

            # Check user data consistency
            # - - - - - - - - - - - - - -
            be.check(egr)

            # Move to ember position
            # - - - - - - - - - - - -
            xbas += gp['be_int_x'] / 2.0

            # Draw ember:
            # - - - - - -
            bex = be.draw(egr, (xbas, xbas+be_x))

            # Prepare data for the line showing the changes between embers :
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            hazl = be.levels_values('hazl')
            risk = be.levels_values('risk')
            if norm(gp['show_changes']) == 'true':
                rlevs = gp.lst('show_changes')
                hlevs = np.interp(rlevs, risk, hazl)
                bexs.append(bex)
                ahlevs.append(
                    hlevs)  # [a]ll [h]azard-[lev]els = for all requested risk levels and all embers in the group

            # Add lines and marks indicating the confidence levels :
            # - - - - - - - - - - - - - - - - - - - - - - - - - - -
            be.drawconf(egr, xbas)

            # Move 'drawing cursor' to the end of this ember (1/2 ember interval after the colour bar)
            xbas += be_x + gp['be_int_x'] / 2.0

        # Draw the lines showing the changes between embers :
        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        if norm(gp['show_changes']) == 'true':
            c.setStrokeColor(egr.colors['tgrey'])
            c.setDash([3, 3], 1)  # 3 unit on, 2 unit off; the last parameter defines a start point with dashes.
            ahlevs = np.transpose(ahlevs)
            for shlevs in ahlevs:  # for one curve = for a [s]ingle of the requested risk-levels
                beys = [egr.haztocan(shlev) for shlev in shlevs]  # scale to Canvas coordinates
                ymax = egr.haztocan(gp['haz_axis_top'])  # Do not draw line from or to levels above the axis
                for ibe in range(len(beys) - 1):  # Draw, by line segment
                    if beys[ibe] <= ymax and beys[ibe + 1] <= ymax:
                        c.line(bexs[ibe], beys[ibe], bexs[ibe + 1], beys[ibe + 1])
                hlp.addlogmes("Mean hazard / requested risk level: {:.3}".format(np.mean(shlevs)))
            c.setDash([], 0)  # Stop dashes = back to solid, unbroken line (this is from Adobe PDF reference !)

        # Add interval between groups
        # - - - - - - - - - - - - - -
        xbas = xend + gp['gr_int_x']
        mxpos = max(mxpos, xbas)

    # Draw the legend
    # ----------------
    # The ember groups form a "grid". The legend can be
    # - centered at the right of the entire grid (leg_pos = right), and vertical
    # - centered under the entire grid (leg_pos = under), and horizontal
    # - inside the grid, as an additional ember group (leg_pos = in-grid-horizontal or in-grid-vertical)
    # The last case is only permitted as it makes sense, ie. there are several lines in the grid and the last
    # line is incomplete:
    if norm(gp['leg_pos']) != "none":
        if ("in-grid" in gp['leg_pos']) and xbas < mxpos and glines > 1:
            emberbox = [xbas, legy, mxpos - xbas, gry]  # Box inside the grid : x0, y0, xsize, ysize
            isinside = True
        else:
            emberbox = [0, legy, mxpos, glines * gry]  # Box surrounding all embers : x0, y0, xsize, ysize
            isinside = False
        mxpos += egr.drawlegend(emberbox, isinside)
        # drawlegend returns any additional horizontal space used by the legend.

    # Add warning if a critical issue happened
    # ----------------------------------------
    # This will appear on top of the normal page, so first calculate the page height:
    mypos = gry * glines + legy
    # If there is more than one critical issue message, only one is 'stamped' on the graph for now.
    if hlp.getlog("critical"):
        egr.style.alignment = TA_LEFT
        egr.style.fontSize = 9
        egr.style.leading = egr.style.fontSize*1.1
        egr.style.textColor = egr.colors['red']
        msg = "Critical issue! this diagram may be unreliable. Please investigate. \n" \
              + hlp.getlog("critical")[0] + "(...)"
        par = Paragraph(msg, egr.style)
        par.wrap(7 * units.cm, 3 * units.cm)
        par.drawOn(c, 0.5 * units.cm, mypos + 0.2*units.cm)
        mypos += 2.5*units.cm  # Add space to the canvas for this warning

    if len(hlp.getlog("warning")) == 0 and len(hlp.getlog("critical")) == 0:
        c.setKeywords(["No warning messages: perfect"])
    else:
        c.setKeywords(["Warnings: "] + hlp.getlog("warning") + hlp.getlog("critical"))

    # Set page size and finalize
    # --------------------------
    # The min function below is a quick fix to enable case where only a few embers are drawn;
    # it should account for the real size of the colorbar
    c.setPageSize((mxpos, mypos))
    c.setCreator("MakeEmbers " + __version__)
    # Todo: old way cannot work as infile becomes optional :
    # c.setTitle(str(os.path.splitext(os.path.basename(infile))[0]))
    c.setSubject("Embers with palette " + egr.cpal['name'])

    c.showPage()
    c.save()

    return {'outfile': outfile, 'width': str(int(mxpos))}


def readembers(sht, gp=None):
    """
    Get the ember data from a file

    :param sht: A sheet from an Excel workbook containing the data
    :param gp: Graphic Parameters which will work as default values
    :return: (lbes, gp) a set of embers (lbes) and new or updated graphic parameters (gp)
    """
    if gp is None:
        gp = param.ParamDict()
    # Check file format; By default, the format is "Basic" = SRCCL-like (look for the File format in the first 6 rows)
    ffind = [sht.cell(i, 2).value for i in range(1, 7)
             if isinstance(sht.cell(i, 1).value, str) and sht.cell(i, 1).value == "File format"]
    if len(ffind) == 1:
        ffmt = ffind[0].strip()
    else:
        ffmt = "Basic"
    hlp.addlogmes("Format of the main input file: " + str(ffmt))

    # BE data storage
    lbes = []  # list of ember instances (to be filled by reading the data part of the Excel sheet, below)

    be = None  # The ember currently being processed
    be_risk = None
    be_group = ''

    # Specifically ignore the irrelevant warning that openpyxl cannot handle Excel's data validation feature:
    warnings.filterwarnings("ignore", module="openpyxl", message="Data Validation extension")

    # Fullflex file format = from Zommers et al 2020
    # - - - - - - - - - - - - - - - - - - - - - - - -
    ndata = 0  # Will be set to the number of risk levels in the file
    if ffmt == "Fullflex":
        dstate = 'paused'  # Cannot read data until 1) allowed to by the 'Start' keyword and 2) the risk levels are set
        for row in sht.rows:
            key = hlp.stripped(row[0].value)
            name = hlp.stripped(row[1].value)
            inda = [acell.value for acell in row[2:]]  # input data
            if key == 'RISK-INDEX':
                # Get the risk levels for which the file will provide data ('hazard' levels related to the risk levels)
                be_risk = inda
                try:
                    ndata = be_risk.index('ref_to_preind')  # number of risk T(risk) levels for which there is data
                    # There are two additional values in header : ref-to-pre-ind and top_value (see .xlsx file)
                    dstate = 'ready'
                except ValueError:
                    raise Exception("Could not find column 'ref_to_preind' in the header line.")
                del be_risk[ndata:]
                for rlev in be_risk:
                    if isinstance(rlev, str):
                        raise Exception("There seems to be a missing value in the RISK-INDEX. This is not allowed")
                hlp.addlogmes('Read risk-index values:' + str(be_risk))
            elif key == 'START':
                dstate = 'waiting header'
                hlp.addlogmes('Waiting for risk levels / header')
            elif key == 'STOP':
                dstate = 'paused'
                hlp.addlogmes('Paused')
            elif key == 'GROUP' and dstate != 'paused':
                be_group = row[1].value
                hlp.addlogmes('Reading ember group: ' + str(be_group), mestype='title')
            elif key == 'HAZARD-INDICATOR' and dstate == 'waiting header':
                raise Exception("DATA was found before any risk levels / header line - cannot handle this.")
            elif key == 'HAZARD-INDICATOR' and dstate == 'ready':
                hlp.addlogmes('Reading data for: ' + str(name), mestype='subtitle')
                # Create an ember and add it to the list of embers:
                be = emb.Ember()
                lbes.append(be)
                be.name = str(name)
                be.group = be_group
                trans = None
                rhaz = float(inda[ndata])  # Reference hazard level (e.g. temperature) / pre-ind
                # Range of BE validity (do not show colours beyond that)
                # The 'fullflex' format only has an upper range so far, called 'top value' in the sheet;
                #      a range bottom was added later in the basic format and copied here 'just in case'
                be.haz_valid = (float(gp.get('haz_valid_bottom', gp.get('haz_axis_bottom', 0))),
                                float(inda[ndata + 1]) + rhaz)
                be_hazl = []  # temporary storage for hazard-level data within a single ember
                be_risl = []  # temporary storage for risk-level data within a single ember
                if ndata != len(be_risk):
                    return {'error': hlp.addlogfail(
                        "Fullflex fmt: #risk levels does not appear to match #hazard levels")}

                for i, x in enumerate(inda[0:ndata]):
                    if x is not None:
                        be_hazl.append(x + rhaz)
                        be_risl.append(be_risk[i])  # so we skip risk levels with missing data for hazard level

                # Create "standard-format" Transitions (which did not exist in the original 'fullflex' format:
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                #   this is to continue supporting the fullflex format, for legacy reasons)
                itran = -1  # Index of the current transition; -1 means we don't have one yet
                nlevs = len(be_hazl)
                trans_phase_std_names = {'p0': 'min', 'p50': 'median', 'p100': 'max'}
                for ilev in range(nlevs):
                    ctran = int(be_risl[ilev])  # Bottom risk level for this transition (0 = undetect., ...)
                    xtran = -1  # id of transition for top of next level, if any:
                    if (ilev + 1) < nlevs:
                        xtran = np.ceil(be_risl[ilev+1])
                    # if itran = ctran or ctran = xtran, we are not in a new transition yet; otherwise, create one:
                    if itran < ctran < xtran and ctran < 3:
                        # Create new transition:
                        trans = emb.Transition(emb.Transition.risk_names[ctran])
                        be.trans.append(trans)
                        itran = ctran
                        hlp.addlogmes(trans)
                    if trans is None:
                        return {'error': hlp.addlogfail("A transition could not be defined for legacy 'fullflex' fmt'")}
                    # By definition, trans_phase = risk idx - base risk idx; write that in the percentile fmt (p*):
                    trans_phase = "p{:d}".format(int((be_risl[ilev] - itran)*100))
                    # Upgrade that to current standard names, when possible: (that might be generalized?)
                    if trans_phase in trans_phase_std_names:
                        trans_phase = trans_phase_std_names[trans_phase]
                    trans.append_level(trans_phase, be_hazl[ilev], "")
                    hlp.addlogmes(f"{trans_phase}: {be_hazl[ilev]}")

            elif key == 'CONFIDENCE' and dstate == 'ready':
                hlp.addlogmes("CONFIDENCE is not supported; "
                              "please move to the standard format if you need confidence levels.")
            elif key == 'HAZARD-INDICATOR-DEF':
                gp['haz_' + name] = inda[0]  # Those parameters are on the first sheet because they relate to data

    # Basic file format = from IPCC SRCCL sup. mat.
    # - - - - - - - - - - - - - - - - - - - - - - -
    elif ffmt == "Basic" or "Standard":
        # The "Basic" is now becoming the standard format, so we consider renaming it in the future.
        # This format provides 'hazard' data for 3 transitions defined below.

        # List of parameters that can be used on the first sheet (= together with the data):
        # Todo: this is used beyond the original intention and becomes clutered;
        #       rethink: include in paramdefs.md? And/or have source and figure information on a different worksheet?
        bfparams = ['project_name', 'project_source', 'project_revision_date', 'project_version',
                    'source_key', 'source_title', 'source_author', 'source_editor', 'source_year',
                    'source_crossref', 'source_chapter', 'source_figure_number',
                    'source_figure_title', 'source_figure_caption', 'source_figure_nickname', 'source_figure_data',
                    'haz_name', 'haz_name_std', 'haz_unit', 'haz_top_value', 'haz_axis_bottom', 'haz_axis_top',
                    'haz_bottom_value', 'haz_valid_bottom', 'haz_valid_top',
                    'haz_map_factor', 'haz_map_shift', 'be_palette',
                    'leg_title', 'leg_pos', 'software_version_min']

        dstate = 'wait-data'  # File reading status
        # Valid file reading statuses:
        # - wait-data: default condition, first level of file analysis, not expecting a particular kind of data.
        # - reading: inside an ember; expecing a valid ember line
        # - paused: ignores anything until a "START" line is found
        started = False  # True after a first ember was read; used to check global metadata such as req. soft version.
        trans = None
        be_group = u''  # Default ember group name
        metanames = []  # List of names of ember-related metadata
        tr_explanation_row = None  # Optional row for an explanation about the transition (metadata at transition level)
        startmeta = 6

        for irow, row in enumerate(sht.rows):
            if len(row) == 0:
                continue
            cola = hlp.stripped(row[0].value)  # Column A: may optionally contain the name of a group of embers
            colb = hlp.stripped(row[1].value)  # Column B: contains ember name, in the first line of a new ember.
            # if already reading and column D is blank or an ember name is found, an ember ended: prepare for next ember

            if dstate == 'reading' and (hlp.isempty(row[3].value) or not hlp.isempty(colb)):
                # After reading a first ember, we now expect the start of a new ember
                trans = None  # Since this is a new transition, it needs a name before it can be defined
                dstate = 'wait-data'

            if cola == 'START':
                dstate = 'wait-data'
                hlp.addlogmes('Waiting for ember data')
                # Check file compatibility (we should have it now because the main parameters were read)
            elif cola == 'STOP':
                dstate = 'paused'
                hlp.addlogmes('Paused')
            elif cola in bfparams:
                # Read parameter
                gp[cola] = colb
            elif not hlp.isempty(cola) and hlp.isempty(colb) and dstate == 'wait-data':
                # Read group name (data in first column, second column empty)
                be_group = cola
                hlp.addlogmes('Reading ember group: ' + str(be_group), mestype='title')
            elif colb in ['Name', 'Component', 'Name of system at risk']:
                # This line is a table header
                if len(row) > 6:
                    startmeta = 6  # Index of first column potentially containing ember-related metadata.
                    if norm(row[startmeta].value) == "explanation":
                        # There is an 'explanation' column for the transition
                        tr_explanation_row = startmeta
                        startmeta += 1
                    # Get names of ember-related metadata - feature in development (2021); may be improved.
                    metanames = [str(cell.value).strip() for cell in row[startmeta:] if cell.value]
                    metanames = [name.lower().replace(' ', '_') for name in metanames if name != ""]
                    for name in metanames:
                        if name not in ['remarks', 'description', 'keywords', 'long_name',
                                        'inclusion_level', 'references']:
                            hlp.addlogwarn('Unknown ember metadata name: ' + name)
            elif hlp.isempty(cola) and not hlp.isempty(colb) and dstate == 'wait-data':
                # Start new ember
                if not started:
                    # This is the first ember. Check anything related to metadata before starting to read:
                    fver = str(gp['software_version_min'])
                    if fver > __version__:
                        hlp.addlogwarn("The input file requires a version ({}) newer than this app ({})"
                                       .format(fver, __version__), critical=True)
                    started = True
                hlp.addlogmes('Reading data for: ' + str(colb), mestype='subtitle')
                # Create an ember and add it to the list of embers:
                be = emb.Ember()
                lbes.append(be)
                be.name = str(colb)
                be.group = be_group
                # Range of BE validity (do not show colours under/above that;
                # use haz_valid_* if not None, else haz_axis* (which must at least have a default value)
                be.haz_valid = (float(gp.get('haz_valid_bottom', gp['haz_axis_bottom'])),
                                float(gp.get('haz_valid_top', gp['haz_axis_top'])))
                be.hazn = '-' if 'haz_name_std' not in gp.keys() else gp['haz_name_std']  # Hazard metric std name
                # Read optional metadata
                if len(row) > 6:
                    nmeta = min(len(row)-6, len(metanames))  # Metadata needs a name and a value, otherwise ignored
                    for icol, cell in enumerate(row[startmeta:startmeta+nmeta]):
                        be.meta[metanames[icol]] = cell.value
                dstate = 'reading'  # Now ready to read data for that ember

            if dstate == 'reading':
                # Try to read data if available, but always read transition name etc.
                trans_phase = norm(row[3].value)
                if trans_phase in trd.phases_syn:  # Old name for the phase => 'translate' to new
                    trans_phase = trd.phases_syn[trans_phase]
                if not hlp.isempty(row[2].value):
                    # Start of a transition
                    trans_name = norm(row[2].value)
                    if trans_name in trd.names_syn:  # Old name for the transition => 'translate' to new
                        trans_name = trd.names_syn[trans_name]
                    conf = row[5].value  # The confidence level, if any, is given at the start of the transition.
                    # (the validity of the confidence level name is checked below, when it is used)
                    trans = emb.Transition(trans_name)
                    if tr_explanation_row:
                        trans.meta['explanation'] = row[tr_explanation_row].value
                    newtrans = True
                else:
                    if trans is None:
                        return {'error': hlp.addlogfail("Input file format error in line {}. "
                                                        "All transitions must start with a 'min' or 'begin' value"
                                                        .format(irow + 1))}
                    conf = hlp.stripped(row[5].value, default="")
                    newtrans = False
                # Trying to read ember data, but we don't have information about the current transition:
                if (trans is None or hlp.isempty(row[3].value)) and not hlp.isempty(row[4].value):
                    hlp.addlogwarn('Input file may be badly formated: data without transition: ' + str(row[4].value))
                trans_phper = trd.phaserisk(trans_phase)
                if trans_phper is None:
                    return {'error': hlp.addlogfail(f"Input file format error: "
                                                    f"unknown transition phase '{trans_phase}' in line {irow + 1}")}

                hazl = row[4].value
                confmessage = f"; conf: {conf}" if not hlp.isempty(conf) else "."
                hlp.addlogmes(f"- {trans.name}/{trans_phase} -> {str(hazl)}{confmessage}")
                if type(hazl) in [float, int]:  # existing (not missing) value
                    if newtrans:
                        be.trans.append(trans)
                    if trans_phase == 'mode':
                        # A very special case used for expert elicitation. To change later for simplification?
                        trans.mode = float(hazl)
                    else:
                        # Addition level to transition
                        conf = norm(conf)
                        trans.append_level(trans_phase, hazl, conf)

    else:
        return {'error': hlp.addlogfail("Unknown input file format:" + str(ffmt))}

    if len(lbes) == 0:
        return {'error':
                hlp.addlogfail("No embers were found in the input file. Suspect a formatting error or incompatiblity.")}

    return {'lbes': lbes, 'gp': gp}
