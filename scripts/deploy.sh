#!/usr/bin/env bash


# Update the version commit id
sed -i "s/'.*'/'$(git log -1 --pretty=format:%h)'/g" frontend/src/components/Version.js

# Spin up backend and frontend services in two tmux sessions
tmux kill-server
tmux new-session -d bash
tmux split-window -h bash
tmux send -t 0:0.0 "python -m pip uninstall recipedex -y; python -m pip install recipedex/." C-m
tmux send -t 0:0.0 "python -m pip uninstall backend -y; python -m pip install backend/." C-m 
tmux send -t 0:0.0 "python -m backend --prod --log WARNING" C-m
tmux send -t 0:0.1 "npm install --prefix frontend" C-m
tmux send -t 0:0.1 "npm run build --prefix frontend" C-m
tmux send -t 0:0.1 "npm run serve --prefix frontend" C-m
tmux -2 attach-session -d
