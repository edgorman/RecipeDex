#!/bin/bash

python -m flake8 backend/
npm run lint --prefix frontend
