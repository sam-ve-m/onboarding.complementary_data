fission spec init
fission env create --spec --name onb-br-complement-env --image nexus.sigame.com.br/fission-onboarding-br-complement:0.1.0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-br-complement-fn --env onb-br-complement-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-br-complement-rt --method PUT --url /onboarding/complementary_data --function onb-br-complement-fn
