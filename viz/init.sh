#!/bin/bash
docker pull jupyter/datascience-notebook
docker run --rm -it -v $(pwd):/root -p 8888:8888 jupyter/datascience-notebook jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/root'

