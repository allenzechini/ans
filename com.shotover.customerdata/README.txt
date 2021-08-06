#!/bin/bash


# Overview
Simple GUI to view customer data

## Why was this buil?
This is intended to be a temporary viewing solution with the goal of porting into AWS or other environment

## How was this buil?
Built using React components for portability.

## How do I use this?
Requires a web server, so we'll start a simple one with python to serve on localhost:8000

You can start one using:
./start_server.sh

or manually with:
python -m http.server 8000
