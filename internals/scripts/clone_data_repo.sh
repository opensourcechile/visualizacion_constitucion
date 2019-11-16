#!/bin/bash
directory=data
repo_url=git@github.com:opensourcechile/constitucion_chile.git
repo_directory=constitucion_chile

cd $directory
git clone $repo_url
cd $repo_directory
git pull origin master
