# HistoryGuessr

## Introduction

The project is a game inspired by Geoguessr (https://www.geoguessr.com/) where the goal is to guess your location on a map from a random position on Google Street View.



Our game would be history-oriented (guessing a year rather than a place) based on images representing known historical events. To do this, we had to gather a large database of images associated with a year. In addition, these images must be known enough to be recognized by everyone.



A game is composed of 10 rounds, each round corresponds to a random year and it is possible to display up to 6 images per round (of the same year). Players will therefore have to guess the year based on the images. Each round earns a number of points. The goal is to have the maximum score at the end of the 10 rounds and invite your friends to achieve a better score by sharing your game which will have exactly the same years and images.



## Installation

Git clone the projet. You will need to have Node.js, Composer & Python already installed.

### Frontend (Angular)

- `cd front`
- `npm ci` : install dependencies.
- `ng serve` : start the front by default on http://localhost:4200/.

### Backend (Laravel)

- `cd back`
- `cp .env.example .env`  : copy & rename the environnement file, you need to edit the database config.
- `php artisan key:generate` : permet de générer une clef pour Laravel.
- `php artisan migrate:fresh` : permet de créer la structure de la base de donnée.
- `php artisan serve` : start the back on the APP_URL, you have put in the `.env` file.

### Data

- `cd other/data-gathering/`
- `python event-data-gathering.py` : load the database with historical events ([DBpedia](https://wiki.dbpedia.org/))
- `python album-data-gathering.py ` :  load the database with album covers ([DBpedia](https://wiki.dbpedia.org/))
- `python film-data-gathering.py ` :  load the database with films, TV shows and animes ([The Movie Database](https://www.themoviedb.org/))

