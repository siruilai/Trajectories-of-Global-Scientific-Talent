# Trajectories of Global Scientific Talent

[![GitHub Pages](https://img.shields.io/badge/Interactive%20Visualization-GitHub%20Pages-bluei.github.io/Trajectories-of-Global-Scientific-Talent/webVis/)
[![Data Source](https://img.shields.io/badge/Data-ORCID%202025-green)](https://doi.org/10.23640/07243.303755](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/siruilai/Trajectories-of-Globalnt)

## Overview

This repository contains the data, analytical code, derived outputs, figures, and interactive visualization associated with the study **Trajectories of Global Scientific Talent**.

The project reconstructs and analyzes the temporal and geographic trajectories of researchers using publicly available ORCID records. It provides a reproducible workflow for processing researcher affiliations and related career information, generating analytical datasets, producing figures, and visualizing the geographic composition and movement of scientific talent over time.

An interactive visualization of the reconstructed data is available at:

**https://siruilai.github.io/Trajectories-of-Global-Scientific-Talent/webVis/**

## Research Objectives

The project is designed to support the study of global scientific talent trajectories by:

- reconstructing researchers' temporal and geographic career records from ORCID data;
- organizing researcher affiliation records into structured analytical datasets;
- examining changes in the geographic distribution of scientific talent over time;
- identifying and summarizing researcher movements across locations;
- producing publication-ready figures and derived data outputs; and
- providing an interactive web-based visualization of researcher flows and geographic composition.

## Repository Structure

```text
Trajectories-of-Global-Scientific-Talent/
├── .github/
│   └── workflows/             # GitHub Actions workflow for GitHub Pages deployment
├── code/                      # Source code for data processing and analysis
├── data/                      # Data used or distributed with the repository
├── data_output/               # Processed and derived analytical outputs
├── fig_output/                # Generated figures
├── webVis/                    # Interactive web visualization
├── requirements.txt           # Python package dependencies
├── settings.json              # Project configuration and path settings
└── talenthubs_analyzer.ipynb  # Main analysis notebook
