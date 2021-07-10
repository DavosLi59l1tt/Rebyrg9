# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This is the boot file for ModelArts platform.
Firstly, the train datasets are copyed from obs to ModelArts.
Then, the string of train shell command is concated and using 'os.system()'
Lastly, the trained result is copyed to obs from ModelArts Platform.
"""
import os
import numpy as np
import datetime
import moxing as mox
import argparse

print(os.system('env'))

if __name__ == '__main__':
    ## Open the print log to check some params.
    os.environ['SLOG_PRINT_TO_STDOUT'] = "1"

    ## Remember the code dir is not the same as work dir on ModelArts Platform!!!
    code_dir = os.path.dirname(__file__)
    work_dir = os.getcwd()
    print("===>>>code_dir:{}, work_dir:{}".format(code_dir, work_dir))

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_url", type=str, default="./output")
    parser.add_argument("--data_url", type=str, default="./dataset")
    config = parser.parse_args()

    print("--------config----------")
    for k in list(vars(config).keys()):
        print("key:{}: value:{}".format(k, vars(config)[k]))
    print("--------config----------")

    local_dir = os.path.join(work_dir, 'dataset')
    os.makedirs(local_dir)

    ## copy dataset from obs to local work directory
    start = datetime.datetime.now()
    print("===>>>Copy files from obs:{} to local dir:{}".format(config.data_url, local_dir))
    mox.file.copy_parallel(src_url=config.data_url, dst_url=local_dir)
    end = datetime.datetime.now()
    print("===>>>Copy from obs to local, time use:{}(s)".format((end - start).seconds))
    files = os.listdir(local_dir)
    print("===>>>Files number:", len(files))

    # unzip
    print("===>>>Begin uncompressing:")
    start = datetime.datetime.now()
    os.system('unzip -q {} -d {}'.format(os.path.join(local_dir, 'cat.zip'), local_dir))
    end = datetime.datetime.now()
    print("===>>>Uncompressing finished: time use:{}(s)".format((end - start).seconds))
    train_dir = os.path.join(local_dir, 'cat')
    files = os.listdir(train_dir)
    print("dir:{}  files:{}".format(train_dir, files))
    print("===>>>Files number:", len(files))

    ## start to train
    start = datetime.datetime.now()
    bash_header = os.path.join(code_dir, 'scripts/run_modelarts_1p.sh')
    bash_command = 'bash %s %s' % (bash_header, code_dir)
    print("bash command:", bash_command)
    os.system(bash_command)
    end = datetime.datetime.now()
    time_used = (end - start).seconds

    os.environ['SLOG_PRINT_TO_STDOUT'] = "1"
    ## Copy learned generator result images to obs directory.
    print("Copy test result images start")
    obs_result_dir = os.path.join(config.train_url, 'result')
    if not mox.file.exists(obs_result_dir):
        mox.file.make_dirs(obs_result_dir)

    work_dir = os.getcwd()
    samples_dir = os.path.join(work_dir, "samples")
    mox.file.copy_parallel(samples_dir, obs_result_dir)
