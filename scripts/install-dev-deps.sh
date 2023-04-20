#!/usr/bin/env bash
pipenv requirements --dev-only > requirements.txt
pip install --requirement requirements.txt
