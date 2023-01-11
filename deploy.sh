fission spec init
fission env create --spec --name onb-br-complement-env --image nexus.sigame.com.br/fission-onboarding-br-complement:0.2.0-0 --poolsize 0 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-br-complement-fn --env onb-br-complement-env --code fission.py --targetcpu 80 --executortype newdeploy --maxscale 3 --requestsperpod 10000 --spec
fission route create --spec --name onb-br-complement-rt --method PUT --url /onboarding/complementary_data --function onb-br-complement-fn
