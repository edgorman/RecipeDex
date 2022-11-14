#!/usr/bin/env bash


tmux kill-server
tmux new-session -d bash
tmux split-window -h bash
tmux send -t 0:0.0 "python -m pip uninstall recipedex -y; python -m pip install recipedex/." C-m
tmux send -t 0:0.0 "python -m pip uninstall backend -y; python -m pip install backend/." C-m 
tmux send -t 0:0.0 "python -m backend --reload --resetdb --log DEBUG" C-m
tmux send -t 0:0.1 "npm install --prefix frontend" C-m
tmux send -t 0:0.1 "npm start --prefix frontend" C-m
tmux -2 attach-session -d
