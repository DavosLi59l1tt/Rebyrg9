#!/bin/sh

python3 ./main.py --phase train --dataset cat --epoch 100 --iteration 100 --batch_size 64 --g_lr 0.0002 --d_lr 0.0002 --img_size 128

if [ $? -eq 0 ] ;
then
    echo "turing train success"
else
    echo "turing train fail"
fi