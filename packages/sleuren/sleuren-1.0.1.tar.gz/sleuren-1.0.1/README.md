# Agent

Server Monitoring (sleuren.com) is a web service that monitors and displays statistics of your server performance.

Agent is OS agnostic software compatible with Python 2.7, 3.5, and 3.6. It's been optimized to have low CPU consumption and comes with an extendable set of useful plugins.

[![Build Status](https://github.com/sleuren/agent/workflows/Agent-Test-And-Deploy/badge.svg?branch=main)](https://github.com/sleuren/agent/actions/workflows/test-and-deploy.yml)

## Documentation

You can find the full documentation at [docs.sleuren.com](https://sleuren.com/docs).

## Automatic Installation (All Linux Distributions)

You can install the default configuration of Sleuren on all Linux distributions with just one click.

1. Connect to your server via SSH.

2. Find your `TOKEN`. To do so, [go to the project installation page](https://sleuren.com/dashboard).

3. Run the following command:

  ```sh
  wget -q -N https://sleuren.com/sleuren.sh && bash sleuren.sh TOKEN
  ```
