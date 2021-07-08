#!/bin/bash
### Apulis Platform command for train (CANN Version-20.2  C76)
## Set Ascend Log Level, if u wanna to print on terminal, you should open 'ASCEND_SLOG_PRINT_TO_STDOUT'. 
export ASCEND_SLOG_PRINT_TO_STDOUT=0
export ASCEND_GLOBAL_LOG_LEVEL=3
export TF_CPP_MIN_LOG_LEVEL=2        ## Tensorflow api print Log Config

currentDir=$(cd "$(dirname "$0")"; cd ..; pwd)
echo "===>>>Python boot file dir: ${currentDir}"

python3 ${currentDir}/main.py \
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