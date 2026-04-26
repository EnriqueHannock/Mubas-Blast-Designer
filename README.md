# Mubas-Blast-Designer

MUBAS BLAST DESIGNER
User Guide
Version 2.0

Prepared by Group 4

Said Ibrahim   |   Enrique Hannock   |   Promise Magola
Mining Engineering Department
Malawi University of Business and Applied Sciences (MUBAS)
Module: Computer Application – Conceptual Development
Supervisor: Dr. Matsimbe
 
1. Introduction

The MUBAS Blast Designer is a desktop application developed by Group 4 of the Mining Engineering Department at the Malawi University of Business and Applied Sciences (MUBAS). The application was designed and built as part of the Computer Application module under the supervision of Dr. Matsimbe. It represents a practical implementation of engineering software tools tailored to the needs of both mining engineering students and practising field engineers operating in open-pit surface bench blasting environments.
Blast design is one of the most critical operations in open-pit mining. Poorly designed blasts result in oversized rock fragments, excessive ground ibration, flyrock hazards, and increased costs associated with secondary breakage and equipment wear. Conversely, well-designed blasts improve fragmentation quality, reduce explosive consumption, and enhance overall productivity. This application provides a structured, formula-driven approach to blast design, enabling users to rapidly compute key blast geometry and charge parameters based on site-specific inputs.

The application is based on the Konya-Langefor empirical blast design method and uses Ammonium Nitrate Fuel Oil (ANFO) as the explosive. It is designed for single-hole deterministic blast calculations and is intended to serve as both a learning tool for engineering students and a quick-reference field calculator for practitioners. The interface is clean, well-labelled, and organised into four functional sections: Design Inputs, Results and Metrics, Fragmentation Prediction, and History.


2. Aim of the Application

The primary aim of the MUBAS Blast Designer is to provide a reliable and easy-to-use blast calculation tool for open-pit surface bench blasting using ANFO explosives. Specifically, the application seeks to:
•	Enable mining engineering students and practitioners to calculate blast geometry parameters quickly and accurately without manual computation.
•	Visualise the relationship between input parameters (hole geometry, rock strength, explosive density) and output results (burden, spacing, stemming, charge weight).

•	Provide a fragmentation prediction curve using the Rosin-Rammler model, helping users understand expected fragment size distributions.
•	Serve as an educational tool that exposes students to real engineering design logic and empirical methods used in professional blast design.
•	Support field engineers in verifying blast designs on-site through a straightforward, portable desktop application.
•	Maintain a session history of all calculations, allowing comparison across multiple design scenarios.

3. Details and Uses of the Application

The MUBAS Blast Designer (version 2.0) is a desktop application built for use on Windows operating systems. It is titled under the program BMEN 5 and carries the branding of the MUBAS Mining Engineering Department. The application requires no internet connection and operates entirely as a local, standalone tool.
The application accepts five primary user inputs: hole diameter (in millimetres), bench height (in metres), rock unconfined compressive strength (UCS in MPa), ANFO density (in kg/m3), and target powder factor (in kg/m3). From these inputs, it computes burden, spacing, stemming, charge length, explosive charge weight per hole, blast volume per hole, and actual powder factor. These outputs are displayed in a clear numerical summary table alongside a schematic hole cross-section diagram.

The application is intended for use in the following scenarios:

•	Academic laboratory sessions and tutorial exercises in blast design courses.
•	Quick field checks during pre-blast planning for open-pit benches.
•	Sensitivity analysis by comparing outputs across varying input parameters.
•	Fragmentation assessment using the built-in Rosin-Rammler distribution model.
•	Training and demonstration purposes when introducing blast design concepts to new engineers or technicians.
The application saves each calculation run to a session history log that shows the time of calculation, all key input and output values, and a pass or fail status for the powder factor tolerance check. This history can be exported or cleared as needed.

4. Significance of the Application

The development of the MUBAS Blast Designer carries significance both academically and practically. From an academic standpoint, it demonstrates that engineering students at MUBAS are capable of conceiving, designing, and implementing functional engineering software tools. The application bridges the gap between theoretical blast design knowledge and practical computational implementation.
From a practical standpoint, the application addresses a real need in the mining industry. Blast design in many small-scale and mid-tier open-pit mines is often performed manually using paper forms or basic spreadsheet tools that offer no validation checks, no visual feedback, and no fragmentation analysis. The MUBAS Blast Designer introduces automatic input validation, powder factor tolerance checking, and graphical fragmentation curves within a single, unified interface.

Key areas of significance include:

•	Production Optimisation: By accurately computing burden and spacing, the tool promotes better fragmentation control, reducing the risk of oversized boulders and secondary blasting costs.
#•	Cost Efficiency: Precise explosive loading calculations help minimise explosive waste and reduce overall blast cost per tonne.
•	Safety Compliance: Input validation and engineering limits embedded in the application help ensure that designs remain within safe and practical bounds.
•	Academic Learning: Students gain a direct visualisation of how input parameters interact with blast geometry through the real-time calculation and graphical outputs.
•	Institutional Branding: The application includes an institution logo URL input field, allowing it to be customised for use under different institutional or corporate identities.

5. User Interface Overview
   
The MUBAS Blast Designer features a two-panel layout. The left-hand panel serves as the persistent sidebar containing navigation links, the institution logo input field, the application name and version, and two collapsible quick reference sections for blasting formulae and constants. The right-hand panel is the main content area, which changes depending on the active section selected from the navigation menu.
The application window includes a standard Windows title bar at the top with minimise, maximise, and close controls. A thin menu bar sits below the title bar and provides access to File, Edit, View, Window, and Help menus. A three-dot icon in the top-right corner of the main panel provides additional display options.


The main screen is divided into the sidebar on the left and the primary content panel on the right. On initial launch, the Design Inputs section is active and the Calculation History panel at the bottom displays a prompt indicating that no calculations have been performed yet.

6. Sidebar Navigation

The sidebar is always visible regardless of which section is active. It contains the following elements from top to bottom:
Institution Logo URL
A text input field at the top of the sidebar allows the user to paste a URL linking to an institution logo image. This field is optional and is provided for institutional customisation. When a valid image URL is entered, the logo will appear in the sidebar above the application name. A small question mark icon next to the field provides tooltip guidance.

Application Name and Version

Below the logo field, the application name ‘BLAST DESIGNER’ is displayed in large text along with the program identifier (BMEN 5) and version number (v2.0). This section identifies the application and its academic context.

Navigation Menu

The Navigation section contains four links that allow the user to switch between the main functional areas of the application:
•	Design Inputs: The primary screen where all input parameters are entered and the calculation is triggered.
•	Results & Metrics: Displays the full computed output including the parameter summary table, hole cross-section diagram, and powder factor match status.
•	Fragmentation: Shows the Rosin-Rammler fragmentation prediction curve and key passing size table.
•	History: Displays the full session history of all calculation runs with timestamps and pass/fail status.

Quick Reference

Two collapsible panels at the bottom of the sidebar provide on-screen reference material. The Blasting Formulae panel lists the key equations used by the application (burden, spacing, stemming, charge weight, powder factor). The Constants Used panel lists the empirical constants applied in the calculations, including the burden factor (Kb = 25), spacing ratio (Ks = 1.25), and the Rosin-Rammler x50 model via UCS scaling. As shown in Figure 2, expanding these panels reveals the formulae and constants directly in the sidebar without navigating away from the current screen.

 
7. Design Inputs Section

The Design Inputs section is the starting point for any calculation. It is divided into three sub-panels arranged horizontally: Hole Geometry, Explosive Parameters, and Run Analysis. Below these panels sits the Calculation History log.

7.1 Hole Geometry

This panel contains three input fields that define the physical geometry of the blast hole and the rock properties:
Input Field	Unit	Default Value	Valid Range	Description
Hole Diameter (D)	mm	90.00	32 to 400 mm	The diameter of the drilled blast hole, corresponding to the drill bit size used on site.
Bench Height (H)	m	9.00	1 to 60 m	The vertical height of the bench being blasted. This is entered directly by the user and represents the working bench face height.
Rock UCS	MPa	45.00	5 to 400 MPa	The Unconfined Compressive Strength of the rock mass. This value is used to select the appropriate burden factor and to scale the median fragment size in the Rosin-Rammler model.

Each field includes decrement and increment buttons (marked with minus and plus signs) allowing the user to adjust values in small steps without typing. Values can also be typed directly into the field. The application will reject values outside the stated valid ranges and display an engineering warning.

7.2 Explosive Parameters

This panel contains two input fields defining the properties of the ANFO explosive and the desired blast intensity:
Input Field	Unit	Default Value	Valid Range	Description
ANFO Density (ρ)	kg/m3	825.00	700 to 1000 kg/m3	The bulk density of the ANFO explosive loaded into the hole. Standard ANFO typically ranges from 800 to 850 kg/m3. Values outside typical ANFO density bounds will be flagged.
Target Powder Factor (PF)	kg/m3	1.00	0.4 to 1.2 kg/m3	The desired explosive consumption per cubic metre of rock. This is a user-fixed design target. The application compares the geometrically calculated actual powder factor against this target and reports the delta value.

7.3 Run Analysis

This panel contains the Run Calculation button. Once all input fields have been filled with valid values, clicking Run Calculation triggers the full calculation sequence. The application will:
1.	Convert hole diameter from millimetres to metres.
2.	Compute burden using B = Kb x D (where Kb = 25).
3.	Compute spacing using S = Ks x B (where Ks = 1.25).
4.	Compute stemming using T = 0.7 x B.
5.	Compute charge length as Lc = H − T.
6.	Compute explosive charge weight per hole using W = (π/4) x D² x ρ x Lc.
7.	Compute blast volume per hole as V = B x S x H.
8.	Compute actual powder factor as PF = W / V.
9.	Compare actual PF against target PF and report the delta.
10.	Run the Rosin-Rammler fragmentation model and update the fragmentation screen.
11.	Append the result to the Calculation History log.

8. Results and Metrics Section
   
After clicking Run Calculation, the user can navigate to the Results & Metrics section to view the full output of the calculation. This section presents results in three areas: the summary metrics bar at the top, the powder factor match banner, the parameter summary table on the left, and the hole cross-section diagram on the right.


8.1 Powder Factor Match Banner

Below the summary bar, a status banner reports the powder factor comparison result. It displays the actual PF, the target PF, the delta value, and indicates whether the result is within the acceptable tolerance of plus or minus 0.05 kg/m3. A green banner indicates a match within tolerance. If the delta exceeds the tolerance, the banner will indicate a mismatch and the user should adjust the input parameters accordingly.

8.2 Parameter Summary Table

The Parameter Summary table on the left lists all parameters, both inputs and computed values, in a single consolidated view. Each row shows the parameter name, its value with unit, and a status label of either INPUT or CALC. INPUT rows are the values entered by the user. CALC rows are values computed by the application. The parameters displayed are: Hole Diameter, Bench Height, Rock UCS, ANFO Density, Burden (B), Spacing (S), Primary Stemming (T), Charge Length (Lc), Blast Volume, and Charge Weight.

8.3 Hole Cross-Section Diagram

On the right side of the Results screen, a scaled schematic diagram illustrates the vertical cross-section of the blast hole. The diagram shows the surface level at the top, the stemming zone immediately below, and the explosive column occupying the lower portion of the hole. Dimensional labels indicate the burden (B) at the top and the bench height (H) along the side. This visual representation helps users verify that the proportions of stemming and charge length are appropriate relative to the total hole depth.

9. Fragmentation Prediction Section

The Fragmentation screen uses the Rosin-Rammler distribution model to predict the fragment size distribution resulting from the blast. This is automatically populated after each calculation run. The screen is divided into the fragmentation curve chart on the left and the model parameters panel with the key passing sizes table on the right.

 
9.1 Rosin-Rammler Fragmentation Curve

The chart plots cumulative passing percentage on the vertical axis against fragment size in millimetres on the horizontal axis. A solid line represents the Single Column charge prediction. A dashed vertical line marks the median fragment size (x50), and a dashed horizontal line marks the 50% passing level. The intersection of these lines identifies x50, which is the fragment size at which half of the material by mass would pass through a screen.
The model parameters panel on the right of the fragmentation screen displays four values derived from the calculation: the median fragment size x50 (in mm), the uniformity index n (a dimensionless value describing the spread of the distribution), the rock strength used (UCS in MPa), and the charge style (Single Column). In the example shown in Figure 4, x50 is 380.0 mm and n is 1.00, indicating a moderately uniform fragment size distribution.

9.2 Key Passing Sizes Table

A table lists the cumulative passing percentage at six standard sieve sizes: 50 mm, 100 mm, 200 mm, 300 mm, 500 mm, and 800 mm. This table provides a quick reference for assessing whether the expected fragmentation meets the crusher feed requirements or loading and hauling constraints of a specific operation. For the example calculation, 8.7% of material is predicted to pass 50 mm and 76.8% passes 800 mm, indicating that a significant proportion of material will require secondary breakage or careful crusher management.
9.3 Chart Interaction Controls
The fragmentation chart includes three control icons in the upper right corner of the chart area. A download icon allows the chart to be saved as an image file. A zoom icon enables closer inspection of specific regions of the curve. A full-screen icon expands the chart to fill the main panel for detailed viewing, as shown in Figure 5 below.

10. History Section

The History section displays a log of all blast design calculations performed during the current session. It allows the user to compare multiple design scenarios and review past calculations without repeating data entry. The history is maintained in memory for the duration of the session only and is cleared when the application is closed or when the user clicks the Clear History button.

10.1 Calculation History Table

The table in the History section records each calculation run with the following columns:
Column	Description

Time	The timestamp (in HH:MM:SS format) at which the calculation was run during the current session.

Dia (mm)	The hole diameter in millimetres as entered by the user.

H Bench (m)	The bench height in metres as entered by the user.

Burden (m)	The computed burden value in metres.

Spacing (m)	The computed spacing value in metres.

Charge (kg)	The computed explosive charge weight per hole in kilograms.

Style	The charge configuration used. Currently always Single Column for this version.

Act. PF	The actual powder factor in kg/m3 as calculated from the geometry.

Tgt PF	The target powder factor in kg/m3 as entered by the user.

PF Status	A pass or fail label indicating whether the actual PF is within the acceptable tolerance of +/- 0.05 kg/m3 of the target PF.

10.2 Download PDF Report

A Download PDF Report button is provided above the history table. Clicking this button generates a portable document format (PDF) report of the most recent calculation results. This report can be saved for documentation, submitted as part of a blast plan, or shared with a supervisor or safety officer. The report includes all input parameters, computed outputs, and the powder factor match status.

10.3 Clear History

The Clear History button at the bottom of the History section removes all entries from the calculation log for the current session. This action is irreversible within the session. Users are advised to download the PDF report or note any important results before clearing the history.

11. Input Validation and Engineering Limits

The MUBAS Blast Designer incorporates automatic input validation to prevent unrealistic or unsafe blast designs from being processed. The following limits are enforced:

Parameter	Minimum Value	Maximum Value	Unit	Validation Action

Hole Diameter (D)	32	400	mm	Values outside this range are rejected. The application displays a warning message and prevents the calculation from running.

Bench Height (H)	1	60	m	Values below 1 m or above 60 m are flagged as unrealistic for open-pit bench blasting.

Rock UCS	5	400	MPa	Values below 5 MPa or above 400 MPa are outside the valid geomechanical range for rock materials.

ANFO Density	700	1000	kg/m3	Values outside the standard ANFO bulk density range are flagged.

Target Powder Factor	0.4	1.2	kg/m3	Values outside the typical ANFO powder factor range prompt an engineering warning.

In addition to rejecting out-of-range values, the application performs the following engineering consistency checks after each calculation:
•	If the stemming height exceeds 40% of the total hole depth, a warning is displayed indicating that excessive stemming may lead to poor fragmentation near the collar.

•	If the computed burden is too small relative to the hole diameter, a warning is displayed indicating an overbreak risk.

•	If the actual powder factor deviates from the target by more than plus or minus 0.05 kg/m3, the powder factor status is marked as FAIL and a mismatch is reported.

•	Negative values are rejected for all input fields.


12. Limitations of the Application

While the MUBAS Blast Designer provides a functional and educationally valuable blast design tool, users should be aware of its limitations before applying results in a professional or operational context:

•	Single Explosive Type Only: The application is designed exclusively for ANFO explosive. It does not support emulsions, heavy ANFO blends, ANFO mixtures, slurries, or any other explosive type. Sites using alternative explosives will need separate tools.

•	Single Hole Design: The application calculates parameters for a single representative blast hole. It does not account for multi-row blast patterns, delay timing sequences, or the interaction effects between adjacent holes.

•	No Vibration Prediction: Ground vibration prediction is not included in the current version. The application does not calculate Peak Particle Velocity (PPV) or assess vibration compliance against regulatory limits.

•	No Flyrock Prediction: Flyrock risk assessment and prediction models are not incorporated. Users must perform separate flyrock risk evaluations as required by local mining regulations.

•	Vertical Holes Only: The application assumes that all blast holes are drilled vertically. Inclined drilling, which is common in many modern open-pit operations for improved burden control and face stability, is not supported.

•	Dry Holes Only: ANFO is only suitable for use in dry blast holes. The application assumes dry hole conditions and does not provide guidance for pumped emulsives or water-resistant explosives in wet conditions.

•	No Subdrilling Input: The application assumes that any subdrilling is incorporated within the total hole depth entered by the user. Subdrilling is not calculated separately.

•	No Deck Charging: Decked charge designs, where stemming is placed between two separate explosive columns in a single hole, are not supported.
•	Uniform Rock Mass Assumption: The Konya empirical method used in the application assumes a uniform, isotropic rock mass. It does not account for geological discontinuities, weak zones, variable rock strength with depth, or structural anisotropy.
•	No Delay Timing Design: The application does not provide blast timing or initiation sequence design. Delay timing, which is critical for controlling ground vibration and achieving optimal fragmentation in multi-row patterns, must be designed separately.
•	Session-Based History Only: The calculation history is stored in memory only for the duration of the current session. No data is saved to disk automatically. Users must download the PDF report before closing the application if they wish to retain their results.
•	Empirical Constants Fixed: The burden factor Kb of 25 and spacing ratio Ks of 1.25 are fixed constants in the application. In practice, these constants may vary depending on rock type, explosive energy, and local blasting experience. The application does not allow the user to override these constants.

13. Step-by-Step Operating Procedure

The following procedure describes how to use the MUBAS Blast Designer to perform a complete blast design calculation from launch to output.
12.	Launch the application by double-clicking the MUBAS Blast Designer executable file. The application will open and display the Design Inputs screen.
13.	Optionally, paste an institution logo URL into the Institution Logo URL field at the top of the sidebar to personalise the display.
14.	On the Design Inputs screen, locate the Hole Geometry panel. Enter the Hole Diameter in millimetres, the Bench Height in metres, and the Rock UCS in MPa. Use the plus and minus buttons or type directly into the fields.
15.	In the Explosive Parameters panel, enter the ANFO Density in kg/m3 and the Target Powder Factor in kg/m3.
16.	Verify that all values are within the valid ranges specified in Section 11. Correct any out-of-range entries before proceeding.
17.	Click the Run Calculation button in the Run Analysis panel. The application will perform the full calculation sequence and update all output panels.
18.	Navigate to the Results & Metrics section using the sidebar menu. Review the summary metrics bar, check the powder factor match banner, examine the parameter summary table, and inspect the hole cross-section diagram
19.	Navigate to the Fragmentation section using the sidebar menu. Review the Rosin-Rammler curve, note the x50 value, and check the key passing sizes table to assess fragmentation suitability.
20.	If required, return to the Design Inputs screen, adjust the input parameters, and run the calculation again. Each run will be added to the Calculation History log.
21.	Navigate to the History section to compare multiple calculation results. Review the PF status column to identify passing designs.
22.	If a satisfactory design has been achieved, click Download PDF Report to save the results as a PDF file for documentation and reporting purposes.
23.	When finished, click Clear History if the log is no longer needed, or close the application.
14. Quick Reference: Formulae and Constants
The following formulae are used internally by the application. They are also available in the expandable Blasting Formulae panel in the sidebar.
Parameter	Formula	Description

Burden (B)	B = Kb x D	Kb = 25 (empirical burden factor); D = hole diameter in metres.
Spacing (S)	S = Ks x B	Ks = 1.25 (spacing ratio).
Stemming (T)	T = 0.7 x B	Primary stemming height.
Charge Length (Lc)	Lc = H - T	H = bench height; T = stemming height.
Charge Weight (W)	W = (π/4) x D² x ρ x Lc	ρ = ANFO density; Lc = charge length.
Blast Volume (V)	V = B x S x H	Rock volume broken per hole.
Powder Factor (PF)	PF = W / V	Actual powder factor in kg/m3.

Constant	Value	Description

Kb (Burden Factor)	25	Empirical constant in Konya method for typical rock conditions.
Ks (Spacing Ratio)	1.25	Typical spacing-to-burden ratio for single-row bench blasting.
PF Tolerance	+/- 0.05 kg/m3	Acceptable deviation between actual and target powder factor.
Stemming Coefficient	0.7	Fraction of burden used to determine stemming height.

15. Glossary of Terms

Term	Definition
ANFO	Ammonium Nitrate Fuel Oil. A widely used bulk explosive consisting of prilled ammonium nitrate and fuel oil. Suitable for dry hole conditions in open-pit blasting.
Bench Height	The vertical distance from the crest of the blast bench to the floor level immediately below. This defines the working face height.
Burden (B)	The perpendicular distance from the blast hole axis to the nearest free face. A critical blast design parameter controlling fragmentation and blasting efficiency.
Charge Length (Lc)	The length of the explosive column within the blast hole, measured from the bottom of the hole to the base of the stemming zone.
Hole Diameter (D)	The diameter of the drilled blast hole, determined by the drill bit size.
Powder Factor (PF)	The mass of explosive consumed per unit volume of rock broken, expressed in kg/m3. A measure of explosive intensity and cost.
Rosin-Rammler Model	A statistical distribution model used to predict fragment size distributions in blasted rock. Characterised by the median fragment size x50 and the uniformity index n.
Spacing (S)	The distance between adjacent blast holes within the same row, measured perpendicular to the burden direction.
#Stemming (T)	Inert material (typically crushed stone or drill cuttings) placed above the explosive column to confine explosive gases and reduce air blast and flyrock.
UCS	Unconfined Compressive Strength. A geomechanical property of rock expressing its resistance to axial loading without lateral confinement. Used as a proxy for rock hardness and blastability.
x50	The median fragment size in the Rosin-Rammler model. It is the fragment size at which 50% of the blasted material by mass is predicted to pass through a screen.


End of User Guide

