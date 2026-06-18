# Energy Meteorology: The synoptic meteorology impacting renewable energy supply and demand

**Project Leads**
* Michael Barnes (michael.barnes@monash.edu; GitHub: weathermanbarnes)
* Chenhui Jin (chenhui.jin@monash.edu; GitHub: chenhui-jin)
* Cindy Nguyen-Dang (cindy.nguyendang@monash.edu; GitHub: )
* Dakota Forbis (dakota.forbis@monash.edu; GitHub: ForbisDakota)

**Project members:**
* Nico Keeghan (nkee0001@student.monash.edu; GitHub: nkeeghan)
* Blake Xu (blake.xu@anu.edu.au; Github: Ic-berg)
* Xinhui Wang (xinhui.wang@utas.edu.au; Github: Taleofpigs)
* Sam Dahl (s.dahl@unsw.edu.au; Github: samcdahl)
* Quentin Rossier (q.rossier@student.unsw.edu.au, Github: qro4)

* Paushali Deb (paushalideb.paushalideb@utas.edu.au; Github:PaushaliDeb)
* Sibyl Cheng (siby.cheng@unsw.edu.au; Github:sibylcheng)
* Linyuan Sun (linyuan.sun@unsw.edu.au; GitHub: Linyuan-Sun)
* Samuel Marcus (Samuel.Marcus@monash.edu; Github SamuelMarcus-cell)
* Emma Fitzgerald (emma.fitzgerald@anu.edu.au; Github: Emma4033)

**Subproject 1: Synoptic Meteorology of Wind Droughts**
* Which weather regimes, or sequences of regimes, relate to wind droughts/lulls of different durations, intensities etc?
* Does ENSO change the above relationship?
* Which weather features drive wind droughts?

*Task list*
* Create a climatology of wind drought over Australia. Wind drought at a grid point is when the daily mean 100 m wind speed in ERA5 < 25th percentile for 3 days
* Test sensitivies to climatology
  - Test 10 m wind speeds
  - Test absolute thresholds (3 m/s, 8 m/s)
  - Including cut-out in wind drought (25 m/s)
  - Testing BARRA vs ERA5
  - Using Wind capacity factor thresholds (0.1, 0.2)
  - Hourly wind droughts definitions? Night-time peak only?
* Statistics / analyses of wind droughts
  - Regional differences (state-based, land versus offshore?)
  - Size
  - Duration
  - Correlation to windy areas for wind drought-prone areas?
* Synoptic characteristics
  - Weather objects (using attribution code)
  - Weather regimes (daily)
 
**Slides**  
1. Climatology/seasonal cycle/thresholding/data problems  (Sam/Quentin)
2. Regimes of wind droughts (Nico/Quentin)
3. Weather objects including cyclones, possibly also TCs (Blake/Xinhui)
4. ENSO (Quentin)
5. Wrap-up slides/main key points/issues (all)

Link: https://docs.google.com/presentation/d/1sEhjPGqmAoeivRUKjAe9fuKgEw0omM1SHk9JWqh25Wc/edit?slide=id.p#slide=id.p

**Subproject 2: Synoptic Meteorology of Energy Demand** 
* How do the Australian weather objects relate to energy demand in Australian capital cities and major towns?
* What are the trends in energy demand and their relationships to weather objects?
* How does energy demand relate to weather regimes?

Google slides: https://docs.google.com/presentation/d/1IvGd6sj0gboNPYQs6ZyMqMz4z-6lE8k0JtGOHd5P5yI/edit?usp=sharing

**Bonus Project: Seasonal Predictability of Energy Meteorology** (Required NCI project: ux62)
* Does the wind-regime relationship (of SP-1) hold in ACCESS-S2?
* How predictable are the frequencies and/or sequences of regimes that drive wind drought?

## References
Energy Demand: Richardson et. al (2024): https://iopscience.iop.org/article/10.1088/1748-9326/ad9b3b

Weather object: Sprenger et al. (2017): https://journals.ametsoc.org/view/journals/bams/98/8/bams-d-15-00299.1.xml

Weather types: Barnes et. al. (2025): https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JD043873


## Contributing Guidelines

> The group will decide how to work as a team. This is only an example. 

This section outlines the guidelines to ensure everyone can work and collaborate. All project members have write access to this repository, to avoid overlapping and merge issues make sure you discuss the plan and any changes to existing code or analysis.

### Project organisation

All tasks and activities will be managed through GitHub Issues. While most discussions will take place face-to-face, it is important to document the main ideas and decisions on an issue. Issues will be assigned to one or more people and classified using labels. If you want to work on an issue, comment and make sure is assigned to you to avoid overlapping. If you find a problem in the code or a new task, you can open an issue. 

### How to collaborate

* **Main branch:** We want to keep things simple, if you are working on a notebook alone you can push changes to the main branch. Make sure to 1) only add and ccommit that file and nothing else, 2) pull from the remote repo and 3) push.

* **Working on a branch:** if you want to fix or propose a change to someone else code you will need to create a branch and open a pull request. Make sure you explain your suggestion in the pull request message. 

## How to cite

> add here citation after you deposit the repo on zenodo

------------------------------------
This is a ![](https://github.com/21centuryweather/research-project-template/raw/main/img/Logo_black_text.png) project.
