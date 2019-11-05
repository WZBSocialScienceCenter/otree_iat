# Implicit Association Test (IAT) experiment for oTree

November 2019, Markus Konrad <markus.konrad@wzb.eu> / [Berlin Social Science Center](https://wzb.eu)

## Introduction

This repository contains an application for [oTree](http://www.otree.org/) ([Chen et al. 2016](http://dx.doi.org/10.1016/j.jbef.2015.12.001)) which implements the Implicit Association Test (IAT) experiment ([Greenwald et al. 1998](https://psycnet.apa.org/buy/1998-02892-004)).

Makes use of the [otreeutils](https://github.com/WZBSocialScienceCenter/otreeutils) package ([Konrad 2018](https://doi.org/10.1016/j.jbef.2018.10.006)).

**Trial block introduction:**

![trial block intro](_doc_imgs/iat1.png)

**A trial:**

![a trial](_doc_imgs/iat2.png)

## Features and limitations

- stimuli and trial blocks easily adjustable (see configuration)
- precise measurement of responses in milliseconds
- progress bar showing advancement of trials for each participant 
- each measurement is stored individually in the database
- live view of measurements during experiment in oTree's data view 
- requires keyboard for responses but may be extended to work on mobile devices as well
- results are transferred to server at the end of each *round* (each round or *block* consists of several trials), *not* after each trial

## Requirements

- Python 3.5 or higher (tested with Python 3.6)
- otree 2.1.41
- otreeutils 0.9.1

You can install the exact requirements using *pip*: `pip install -r requirements.txt`

## Configuration

### Stimuli and trial blocks

For your own experiment, you probably want to exchange the stimuli and adjust the trials. You can do so in `iat/models.py` by editing `STIMULI`, `STIMULI_LABELS` and `BLOCKS`.

### Further configuration via `Constants`

The `Constants` class in `iat/models.py` contains further configuration settings such as the number of blocks (`num_rounds`) and the keys on the keyboard that are used for input. 


## Code structure and page sequence

### Models

A custom `Trial` class is defined in `iat/models.py` that stores information for each trial per player such as displayed stimulus and participant's response. The trials are set up in `creating_session()` in class `Subsession` where the stimuli are loaded depending on the block definition and their order is randomized. 

### Pages and templates

The page sequence consists of three classes in `iat/pages.py`:

1. `Intro`
2. `IATPage`
4. `Outro`

The test is then implemented in `IATPage`, especially in the JavaScript functions of the HTML template. The randomized `Trial` objects are loaded for the participant for the given round and passed to the template where they are displayed. During the test, the response times and keys are recorded and submitted when the next block is loaded or all blocks are finished. The submitted trial responses are handled and stored to the database in the method `IATPage.before_next_page()`.

## Data export

Since the measurements are stored using the custom data model `Trials` (see [this blog post](https://datascience.blog.wzb.eu/2016/10/31/using-custom-data-models-in-otree/) or [Konrad 2018](https://doi.org/10.1016/j.jbef.2018.10.006) for more on custom data models with oTree), the data is not exported automatically using oTree's data export page. However, two methods are provided to obtain the data in hierarchically structured JSON format:

1. You can access the page `https://<SERVER>/custom_export/` (e.g. `http://localhost:8000/custom_export/` on a local development machine) which, after logging in, lets you download the data.
2. You can use the `data_exporter.py` script, e.g. by executing `python data_exporter.py my_data.json` in the terminal, which will store the JSON data to `my_data.json`.

For later processing of the JSON data, you may use the `jsonlite` package for R or the built-in `json` module in Python.

## Tests

Automated tests are implemented in `iat/tests.py` and can be run via `otree test iat`.

## License

Apache License 2.0. See LICENSE file.
