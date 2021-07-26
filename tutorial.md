## BigGAN-Tensorflow<a name="section1358541031613"></a>
BigGAN 是一个经典的图像生成网络，DeepMind于2019年提出了BigGAN（Large Scale GAN Training For High Fidelity Natural Image Synthesis）缩小由GANs生成的图像与来自ImageNet数据集的真实世界图像之间的保真度和多样性的差距。BigGAN以最大规模训练生成性对抗网络，并研究了此种规模下特有的不稳定性。Ascend提供的BigGAN是基于TensorFlow实现的版本。

## ModelArts/OBS/Pycharm ToolKit的关系
在正式开始介绍如何操作之前，要跟大家解释一下在ModelArts上训练该如何存放数据。ModelArts是个执行训练任务的云服务平台，那想要执行训练肯定要先把数据集和训练脚本都传到云上。但是ModelArts本身是不带存储功能的，这就引出了在华为云上的一个存储服务OBS和Pycharm ToolKit插件工具。

<div align=center><img src="https://images.gitee.com/uploads/images/2021/0223/173950_6be6a898_1482256.png "/></div>
- ModelArts平台
    Modelarts平台是华为云面向AI开发者的一站式开发平台，它能够支撑开发者从数据到AI应用的全流程开发过程。包含数据处理、模型训练、模型管理、模型部署等操作，并且提供AI Gallery功能，能够在市场内与其他开发者分享模型。
 - 对象存储服务OBS   
    对象存储服务（Object Storage Service，OBS）是一个基于对象的海量存储服务，为客户提供海量、安全、高可靠、低成本的数据存储能力。
 - Pycharm ToolKit插件
    由于AI开发者会使用PyCharm工具开发算法或模型，为方便快速将本地代码提交到公有云的训练环境，ModelArts提供了一个PyCharm插件工具PyCharm ToolKit，协助用户完成代码上传、提交训练作业、将训练日志获取到本地展示等，用户只需要专注于本地的代码开发即可。

OBS可以把它理解为云上的一块大硬盘。ModelArts作为训练平台，数据集(训练脚本也可以)要从这里取。结合上边的图，当在本地Pycharm开发工具上开发的代码，通过Pycharm ToolKit向ModelArts提交训练任务（训练代码）时，同时需要从OBS下载(拉取)训练数据。同时，训练过程中的打印信息可以回传到Pycharm ToolKit中控制台显示，并且训练结果和文件可以往OBS上存储。

## 快速上手
- 环境准备
  
  **步骤1**，下载软件。包括Pycharm软件，Pycharm toolkit插件以及OBS Browser+，参看 [Modelarts官方链接](http://support.huaweicloud.com/tg-modelarts/modelarts\_15\_0001.html)。同时共享了[IDE Pycharm ](https://zhonglin-public.obs.cn-north-4.myhuaweicloud.com/software/pycharm-community-2020.2.3.exe)，[Pycharm toolkit插件](https://zhonglin-public.obs.cn-north-4.myhuaweicloud.com/software/Pycharm-ToolKit-2.1.zip)和[OBS Browser+](https://zhonglin-public.obs.cn-north-4.myhuaweicloud.com/software/OBSBrowserPlus-HEC-win64.zip)供大家快速下载。

  **步骤2**，创建访问密钥（AK和SK）。详细的创建流程[可参考资料](https://support.huaweicloud.com/tg-modelarts/modelarts_15_0004.html)。(如果没有注册华为云，需要注册)

  **步骤3**，软件安装。IDE Pycharm 和 OBS Browser+正常安装即可，但[Pycharm ToolKit插件的安装参看文档链接](https://support.huaweicloud.com/tg-modelarts/modelarts_15_0003.html)，并使用步骤2中的AK和SK进行配置，[详见指导链接](https://support.huaweicloud.com/tg-modelarts/modelarts_15_0005.html)。
  
  **步骤4**，使用AK和SK密钥登入OBS。运行已经安装的OBS，使用步骤2获取的密钥登入OBS。
  ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/153423_2b88480e_1482256.png "屏幕截图.png")
  
- 下载数据集和训练代码
    
    训练的部分数据集和训练代码可以通过[链接下载](https://zhonglin-public.obs.cn-north-4.myhuaweicloud.com/BigGAN.rar)到本地，并解压到当前文件夹。BigGAN压缩包下有源码BigGANProject和数据集zip。数据集cat.zip不用解压。

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
    
    可以在Pycharm的界面上看到如下截图的打印。

    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/161847_262910b0_1482256.png "屏幕截图.png")

    同时，为了评判GAN网络生成器Generator当前已学习的情况，在训练过程中设置了每500个迭代保存了生成器的结果。保存的数据可以在已配置的OBS PATH路径下的result文件夹查看，本示例设置的OBS PATH路径为 **/linccnu/log**
    
    <div align=center><img src="https://images.gitee.com/uploads/images/2021/0312/094836_9bdcf8ed_1482256.png"/></div>
    将result文件夹从OBS下载到本地磁盘，可以看出随着迭代次数的不断增加，生成器中猫的信息越丰富。
    
    <div align=center><img src="https://images.gitee.com/uploads/images/2021/0312/092610_b9561590_1482256.png"/></div>
    
    **输入图片数据**是随机数

    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0311/204153_fa3e407c_1482256.png "BigGAN_train_00_00000.png")

    **1个Epoch**时的结果

    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0311/204201_23bcb68e_1482256.png "BigGAN_train_01_00000.png")

    **3个Epoch**时的结果

    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0311/204210_cea1cb65_1482256.png "BigGAN_train_03_00000.png")

    **9个Epoch**时的结果

    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0311/204218_47012885_1482256.png "BigGAN_train_09_00000.png")

    值得注意的是，上述效果是在默认训练Epoch数为10，训练耗时大概需要30 minus情况下得到的。如果想要生成更丰富的结果，开发者可以在run_modelarts_1p.sh脚本中修改epoch数的值。但需要提醒的是，链接中获取的cat数据集，只是[**官方数据集**](https://www.kaggle.com/crawford/cat-dataset)的一部分。如需训练最终想要的结果，需要下载全量数据集进行多个Epoch的训练。

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

    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/163515_e9fc5865_1482256.png "屏幕截图.png")

   同时，更多详细的基于pycharm toolkit工具指南，可以参看链接[https://support.huaweicloud.com/tg-modelarts/modelarts\_15\_0007.html](https://support.huaweicloud.com/tg-modelarts/modelarts_15_0007.html)

5. 日志问题

   当前的模型的训练日志，可以通过IDE打屏，pycharm当前工程的文件夹MA\_LOG获取，甚至可以在配置界面上设置的log日志路径下获得。

    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/174646_c4be361c_1482256.png "屏幕截图.png")
    
    ![输入图片说明](https://images.gitee.com/uploads/images/2021/0223/161213_8dfb371f_1482256.png "屏幕截图.png")

6. NPU利用率
当前网络是否下沉到昇腾Ascend910上训练，最直观的方法是在[ModelArts界面](https://console.huaweicloud.com/modelarts/?region=cn-north-4#/trainingJobs)上查看当前训练任务上的资源占用情况。如果NPU曲线的值不为0，那么肯定是下沉到了NPU上训练了。
![npu利用率](https://images.gitee.com/uploads/images/2021/0209/114309_f233454c_1482256.png "npu利用率.png")