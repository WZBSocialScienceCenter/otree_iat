# Implicit Association Test (IAT) experiment for oTree

November 2019, Markus Konrad <markus.konrad@wzb.eu> / [Berlin Social Science Center](https://wzb.eu)

## Introduction

This repository contains an application for [oTree](http://www.otree.org/) ([Chen et al. 2016](http://dx.doi.org/10.1016/j.jbef.2015.12.001)) which implements the Implicit Association Test (IAT) experiment ([Greenwald et al. 1998](https://psycnet.apa.org/buy/1998-02892-004)).

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
- otree 2.1.41 or higher

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

If you have at least otree 3.0.0 you can export the data from the Data page, via the _iat (custom)_ links.

## Tests

Automated tests are implemented in `iat/tests.py` and can be run via `otree test iat`.

## License

Apache License 2.0. See LICENSE file.
