#!/bin/bash

python -m pytest backend/tests -svv
npm run test --prefix frontend
