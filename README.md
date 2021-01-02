<h1 align="center" font> <b><i>Gender Changer w/ CycleGAN </i></b> 👫</h1>

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-2.1.0-red.svg?cacheSeconds=2592000" />
  <img src="https://img.shields.io/badge/python-%3E%3D3.7.7-orange.svg" />
  <img src="https://img.shields.io/badge/pytorch-%3E%3D1.7.0-yellow.svg" />
  <img src="https://img.shields.io/badge/torchvision-%3E%3D0.8.0-green.svg" />
  <a href="https://ainote.tistory.com/7" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-Yes-blue.svg" />
  </a>
  </a>
   <a href="https://github.com/myoons/CycleGAN-Gender-Changer/graphs/commit-activity" target="_blank">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-Yes-darkblue.svg" />
  </a>
  <a href="#" target="_blank">
    <img alt="License: Myoons" src="https://img.shields.io/badge/License-Myoons-purple.svg" />
  </a>
</p>

<br/>
<br/>

## 👤 _**Author : Myoons**_
* **[Github](https://github.com/myoons)**
* **[Website](https://ainote.tistory.com/)**

</br>
</br>

## 🌈 _**Motivation : To give pleasure to friends**_
_FUN is the best! It's always thrilling._

</br>
</br>

## 💻 _**GPU : TITAN RTX**_
_CycleGAN requires quite large memory of GPU. So local GPU was not able to train the current model. I borrwowed a server from school and used [TITAN RTX](https://www.nvidia.com/ko-kr/deep-learning-ai/products/titan-rtx/). Thanks KAIST!_ 😊 

</br>
</br>

## 📁 _**Dataset : Korean Celebrities**_
_Since the purpose of the project was to give pleasure to my friends, I needed a model that was appropriate to Koreans. So I collected Korean Celebrities Images as Dataset. I crawled images with [Selenium](https://www.selenium.dev/) and used [Face Recognition](https://github.com/ageitgey/face_recognition) to crop the face in the images._

_**Man : **_
<br/>
_**Woman : **_

_[Dataset Link](https://drive.google.com/drive/folders/1mCUy34p05QY6qLG33nyN0IMBMKsFRZHP?usp=sharing)_

</br>
</br>

## 🔧 _**Training**_
### _**1. Install Repository**_

_You can install this repository using `git clone`_

    git clone https://github.com/myoons/CycleGAN-Gender-Changer.git


<br/>

### _**2. Setup Dataset**_
_Download the dataset from [Google Drive](https://drive.google.com/drive/folders/1mCUy34p05QY6qLG33nyN0IMBMKsFRZHP?usp=sharing)_
<br/>
_Then build the dataset by setting up the following the directory structure._

    ├── datasets
    |   ├── <dataset_name>         # i.e. genderchange
    |   |   ├── train              # Training
    |   |   |   ├── A              # Contains domain A images (i.e. Man)
    |   |   |   └── B              # Contains domain B images (i.e. Woman)
    |   |   └── test               # Testing
    |   |   |   ├── A              # Contains domain A images (i.e. Man)
    |   |   |   └── B              # Contains domain B images (i.e. Woman)

<br/>

### _**3. Train!**_

    python train.py --dataroot datasets/<dataset_name> --cuda

_This command will start a training session using the images under the dataroot/train directory with the hyperparameters that showed best results according to CycleGAN authors._

_If you don't own a GPU remove the --cuda option, although I advise you to get one!_

<br/>
<br/>

##  📟  _**Tensorboard**_
    tensorboard --logdir ./logs

_You can watch your experiments' progress by runing tensorboard_

<br/>
<br/>

## 📁 _**Major Flags**_
### _1. --n_epochs : Number of epochs in training_
_1. Default : 400_
<br/>
_2. Type : Int_

<br/>

### _2. --batchSize : Size of Batch_
_1. Default : 10_
<br/>
_2. Type : Int_

<br/>

### _3. --size : Size of Image Crop (Squre Assumed)_
_1. Default : 256_
<br/>
_2. Type : Int_

<br/>

### _4. --dataroot : Root Directory of Dataset_
_1. Default : Input as Arugment_
<br/>
_2. Type : Str_

<br/>

### _5. --input_nc / --output_nc : Number of channels of input / output data_
_1. Default : 3_
<br/>
_2. Type : Int_

<br/>



## 🔗 _**References**_

<br/>

_1. [Paper](https://arxiv.org/pdf/1703.10593.pdf)_ <br/>
_2. [Base Code](https://github.com/aitorzip/PyTorch-CycleGAN)_ <br/>
_3. [Face Recognition](https://github.com/ageitgey/face_recognition)_ <br/>
_4. [Project Description](https://ainote.tistory.com/7)_ <br/>
_5. [CycleGAN Home Page](https://junyanz.github.io/CycleGAN/)_ <br/>
_6. [CycleGAN Description Video](https://www.youtube.com/watch?v=Fkq_f3dS9Cqw&t=2401s)_ <br/>
