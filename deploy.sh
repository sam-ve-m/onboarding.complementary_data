#!/bin/bash
fission spec init
fission env create --spec --name complement-env --image nexus.sigame.com.br/fission-async-cx:0.0.1 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name comp-fn --env complement-env --src "./func/*" --entrypoint main.complementary_data --executortype newdeploy --maxscale 1
fission route create --spec --name compd-rt --method POST --url /onboarding/complementary_data --function comp-fn
