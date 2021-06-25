## BigGAN-Tensorflow<a name="section1358541031613"></a>
Simple Tensorflow implementation of "Large Scale GAN Training for High Fidelity Natural Image Synthesis" (BigGAN)

## 快速上手
- 环境准备
  
  **步骤1**，下载软件。包括Pycharm软件，Pycharm toolkit插件以及OBS Browser+，参看 [Modelarts官方链接](http://support.huaweicloud.com/tg-modelarts/modelarts\_15\_0001.html)。同时共享了[IDE Pycharm ](https://zhonglin-public.obs.cn-north-4.myhuaweicloud.com/software/pycharm-community-2020.2.3.exe)，[Pycharm toolkit插件](https://zhonglin-public.obs.cn-north-4.myhuaweicloud.com/software/Pycharm-ToolKit-2.1.zip)和[OBS Browser+](https://zhonglin-public.obs.cn-north-4.myhuaweicloud.com/software/OBSBrowserPlus-HEC-win64.zip)供大家快速下载。

  **步骤2**，创建访问密钥（AK和SK）。详细的创建流程[可参考资料](https://support.huaweicloud.com/tg-modelarts/modelarts_15_0004.html)。(如果没有注册华为云，需要注册)

  **步骤3**，软件安装。IDE Pycharm 和 OBS Browser+正常安装即可，但[Pycharm ToolKit插件的安装参看文档链接](https://support.huaweicloud.com/tg-modelarts/modelarts_15_0003.html)，并使用步骤2中的AK和SK进行配置，[详见指导链接](https://support.huaweicloud.com/tg-modelarts/modelarts_15_0005.html)。
  
  **步骤4**，使用AK和SK密钥登入OBS。运行已经安装的OBS，使用步骤2获取的密钥登入OBS。
  ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/153423_2b88480e_1482256.png "屏幕截图.png")
  
- 下载数据集和训练代码
    
    训练的部分数据集和训练代码可以通过链接下载到本地，并解压到当前文件夹。BigGAN压缩包下有源码BigGANProject和数据集zip。数据集cat.zip不用解压。
    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/154527_d07136ec_1482256.png "屏幕截图.png")
    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/154703_99054883_1482256.png "屏幕截图.png")

- 数据集部署

    在"华北-北京4"区域创建OBS桶，并将下载的数据集cat.zip上传到OBS中的某个桶路径中。如下截图是当前我的路径。
    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/155718_1c07454a_1482256.png "屏幕截图.png")

- 训练代码部署(Pycharm)

    在Pycharm工具栏中，选择"ModelArts > Edit Training Job Configuration"，配置插件配置参数。如果使用Modelarts上的常用(Frequently-used)框架/镜像，配置参数详见如下表格；
    |参数   | 数值及说明 |
    |---------|---------|
    |  Job Name | 自动生成，首次提交训练作业时，该名称也可以自己指定 |
    | Algorithm Source | Frequently-used。如果是Custom，配置参数略有差异 |
    |  AI Engine | **Asend-Powered-Engine,  TF-1.15-python3.7-aarch64** |
    |  Boot File Path | 选择本地的训练启动**Python**脚本 |
    |  Code Directory | 选择训练启动脚本所在的目录 |
    |  OBS Path | 输出路径(train_url)，用于存储训练输出模型和日志文件。 **路径需去除开头的 "obs:/"部分**  |
    |  Data Path in OBS | 训练数据在OBS上的路径(data_url)。  **路径需去除开头的 "obs:/"部分**  |
    |  Specifications | 规格，CPU:24vCPUs 96GiB |
    |  Compute Nodes | 训练节点个数，选 1 |
    |  Running Parameters | 其他超参，用分号隔开。比如 batchsize=4;learning_rate=0.01 |

    ![配置参数](https://images.gitee.com/uploads/images/2021/0223/160641_84499cf8_1482256.png "配置参数.png")

    需要注意的是：

    1. 如果想用NPU进行Tensorflow代码训练，那么AI Engine 中必须填写  **Ascend-Powered-Engine**  和 **TF-1.15-python3.7-aarch64** 

    2. "OBS Path"是obs上某个文件夹的路径，用于存放训练输出模型和日志文件。比如我的名下有一个名字为"linccnu"的桶，并希望输出模型和日志存储在下面已经创建的log文件夹中。我们就将该log在obs上的路径复制过来，**并且去除开头的"obs:/"部分**，OBS Path中填 **/linccnu/log**

        ![log日志](https://images.gitee.com/uploads/images/2021/0117/214343_08416265_1482256.png "log日志.png")

    3. "Data Path in OBS"是数据准备阶段存放的模型训练需要的OBS全路径，比如我在obs存放的示例训练数据集截图如下。**注意**，不是每个网络的训练数据集都是按 train 和 val 划分的，此处只是讲解如何配置"Data Path in OBS"参数路径。
       ![训练数据集](https://images.gitee.com/uploads/images/2021/0223/160941_58d97320_1482256.png "训练数据集.png")

        那么在"Data Path in OBS" 我填写**/zhonglin-public/dataset/cat/**。注意没有“**obs:/**”打头的字段。另外，里面的数据可以是原始的jpeg图片，也可以是离线转好的tfrecords数据。如果图片数据量很大，建议害是tfrecords数据，因为小文件在OBS传输时比较费时；同时，在模型训练时，可以分batch将训练数据加载进内存中，否则容易撑爆内存。

- 运行结果
    
    运行成功，可以在Pycharm的界面上看到如下截图的打印。
    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/161847_262910b0_1482256.png "屏幕截图.png")


## 其他<a name="section7271512256"></a>
1. Modelarts的运行机理
   
   Modelarts每启动一个任务，会根据选择的AI Engine配置，创建一个全新的Docker容器，当训练结束或者异常时，会自动销毁该容器和释放占用的NPU资源，并删除上面的代码和数据。
    ![输入图片说明](https://images.gitee.com/uploads/images/2020/1128/192306_80158e80_8267113.png "zh-cn_image_0295927369.png")
2. 关于OBS
  
    **Obs\(Object Storage Service\)对象存储服务是s3协议，我们该路径不能直接在训练代码中使用**，需要使用moxing的接口mox.file.copy\_parallel\([https://support.huaweicloud.com/moxing-devg-modelarts/modelarts\_11\_0005.html](https://support.huaweicloud.com/moxing-devg-modelarts/modelarts_11_0005.html)\)将训练数据从obs文件夹中拷贝到modelarts任务容器中。另外，modelarts创建的NPU模板容器，ModelArts会挂载硬盘至“/cache”目录，用户可以使用此目录来储存临时文件。“/cache”与代码目录共用资源，不同资源规格有不同的容量。其中ascend NPU下具有3T的容量大小。https://support.huaweicloud.com/modelarts\_faq/modelarts\_05\_0090.html

3. 数据拷贝性能问题

    从obs上传tfrecords训练数据到modelarts容器中，性能如何呢？比如上传10G甚至100G的耗时情况。我在本地实操了一遍，写了一个简单类似的代码如下。
    ```
    # copy dataset from obs to local
    start = datetime.datetime.now()
    print("===>>>Copy files from obs:{} to local dir:{}".format(config.data_url, config.cache_data_dir))
    mox.file.copy_parallel(src_url=config.data_url, dst_url=config.cache_data_dir)
    end = datetime.datetime.now()
    print("===>>>Copy from obs to local, time use:{}(s)".format((end - start).seconds))
    files = os.listdir(config.cache_data_dir)
    print("===>>>Files number:", len(files))
    ```

   通过上面这段代码，实测从OBS拉取如下截图的8.3G的数据到modelarts容器本地的耗时大概25s。更大的数据集耗时，比如100G的tfrecords，亲测大概要 3mins。注意，这里建议Copy大文件，比如 tfrecords，压缩包等。

   最后，使用pycharm+modelarts plugin插件提交训练任务后，在web界面上\(https://console.huaweicloud.com/modelarts/?region=cn-north-4\#/trainingJobs\)的“训练管理”—“训练作业”可以看到，刚刚提交的任务。注意，Pycharm IDE上，一次只能提交一个任务。当前普通华为云账户，在modelarts上只能在单个节点上训练。

   [https://console.huaweicloud.com/modelarts/?region=cn-north-4\#/trainingJobs](https://console.huaweicloud.com/modelarts/?region=cn-north-4#/trainingJobs)

    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0117/221713_8b7e0520_1482256.png "屏幕截图.png")

   同时，更多详细的基于pycharm toolkit工具指南，可以参看链接[https://support.huaweicloud.com/tg-modelarts/modelarts\_15\_0007.html](https://support.huaweicloud.com/tg-modelarts/modelarts_15_0007.html)

5. 日志问题

   当前的模型的训练日志，可以通过IDE打屏，pycharm当前工程的文件夹MA\_LOG获取，甚至可以在配置界面上设置的log日志路径下获得。

    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0117/221908_107fe5bc_1482256.png "屏幕截图.png")
    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/161213_8dfb371f_1482256.png "屏幕截图.png")

6. NPU利用率
当前网络是否下沉到昇腾Ascend910上训练，最直观的方法是在[ModelArts界面](https://console.huaweicloud.com/modelarts/?region=cn-north-4#/trainingJobs)上查看当前训练任务上的资源占用情况。如果NPU曲线的值不为0，那么肯定是下沉到了NPU上训练了。
![npu利用率](https://images.gitee.com/uploads/images/2021/0209/114309_f233454c_1482256.png "npu利用率.png")