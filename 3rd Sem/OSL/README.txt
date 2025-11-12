This is the draft for lab reports. Just copy and paste changing the name of the file.



------------------------------------------------
Title: Lab Report LaTeX Format
Author: Souvik Das
------------------------------------------------

Let me walk through it.

This template consists of three folders and one main.txt file

---------------------
1. `Chapters`

The `Chapters` folder consists of

1.1 Frontpage: where all the relevant details of the front page exist. It includes logos, images, and a table stating the student's name and enrollment number.

1.2 Introduction: This section consists of all the sections, tables, images, and equations. 


------------------------
2. `Figures`
 

The Logos folder has the NISER logo and front page image.

------------------------
3. General

The General folder consists of the following:

3.1 Preamble: It comprised all library calls and tikz (library) geometry definitions for the flowchart.

3.2 References: It includes all BibTeX references.

3.3 Settings: The Settings.tex file includes all the formatting definitions of the report. Formattings like titles, sections, lists, color, table of contents, captions, and fonts.

From the Setting.tex, you can alter front page details or even customize every aspect of the lab report.


------------------------
4. main:

The main file calls all the .tex files from `Chapters`, `Figures`, and `General` and builds the report pdf. 

