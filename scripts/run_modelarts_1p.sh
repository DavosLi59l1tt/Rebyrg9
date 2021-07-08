#!/bin/sh
### Modelarts Platform train command
export TF_CPP_MIN_LOG_LEVEL=2        ## Tensorflow api print Log Config
export SLOG_PRINT_TO_STDOUT=0        ## export all logs to stdout terminal print 0:off 1:on

python3.7 ${1}/main.py \
    --phase train \
    --dataset cat \
    --epoch 10 \
    --iteration 1000 \
    --batch_size 64 \
    --g_lr 0.0002 \
    --d_lr 0.0002 \
    --img_size 128

if [ $? -eq 0 ];
then
    echo "BigGAN train success"
else
    echo "BigGAN train fail"
fi