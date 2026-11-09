# ACP Brevet Time Calculator

A Flask web application for calculating ACP (Audax Club Parisien) brevet control times using AJAX.

## About

This is a class project for CIS 322 (Web and Mobile Application Development) at the University of Oregon. The project implements a working ACP brevet time calculator with a web interface, backend calculations, and automated testing.

## Overview

This calculator determines opening and closing times for checkpoints (controls) during ACP-sanctioned brevets. Riders must arrive within the control window or risk disqualification.

## ACP Brevet Rules

**Official Brevet Distances:** 200km, 300km, 400km, 600km, 1000km

Each control has an opening time (earliest allowed arrival) and closing time (latest allowed arrival), calculated based on speed limits.

### Opening Times (Minimum Speed)
| Distance | Speed |
|----------|-------|
| 0–200 km | 15 km/h |
| 200–400 km | 15 km/h |
| 400–600 km | 15 km/h |
| 600–1000 km | 11.428 km/h |
| 1000+ km | 13.333 km/h |

### Closing Times (Maximum Speed)
| Distance | Speed |
|----------|-------|
| 0–200 km | 34 km/h |
| 200–400 km | 32 km/h |
| 400–600 km | 30 km/h |
| 600–1000 km | 28 km/h |
| 1000+ km | 26 km/h |

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python flask_brevets.py
```

Open `http://localhost:5000` in your browser.

## Testing

```bash
pytest tests/ -v
```

## Author

Caileb Rundell
crundell@uoregon.edu
