#!/bin/bash

# This script is used to clean unnecessary generated files/folders.

remove_eggs() {
  # The directory path is sent as the first argument
  cd $1
  rm -rf build
  rm -rf src/*.egg-info
  rm -rf dist
  cd ..
}

# remove build files from components
remove_eggs block_visualizer
remove_eggs simple_visualizer
remove_eggs data_source_ethereum
remove_eggs data_source_twitter
remove_eggs core


# remove db
cd graph_explorer
rm *.sqlite3
cd ..