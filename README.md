# YOLACT-GUI

---

A GUI for YOLACT.

**[Original repo](https://github.com/dbolya/yolact)**

## Installation
- Clone this repo and enter it
    ```Shell
    git clone https://github.com/jiancong0204/yolact-gui
    cd yolact-gui
    mkdir -p data/coco/images        # Stores image dataset
    mkdir -p data/coco/annotations   # Stores data annotations
    mkdir weights                    # Stores trained model
    ```
  
- Setup the environment using anaconda
    ```shell
    # Create a new environment and activate it
    conda create -n youlact python=3.7
    conda activate yolact
    # Install pytorch
    conda install -c pytorch pytorch
    # Install torchvision
    conda install -c pytorch torchvision
    # Install cython
    conda install -c anaconda cython
    # Install other dependencies
    pip install opencv-python pillow pycocotools matplotlib
    # Install PyQt5
    conda install -c anaconda pyqt
    ```
    |Name                    |Version    |
    |:----------------------:|:---------:|
    |cython                  |0.29.21    |
    |matplotlib              |3.3.4      |
    |opencv-python           |4.5.1.48   |
    |pillow                  |8.1.0      |
    |pycocotools             |2.0.2      |
    |pyqt                    |5.9.2      |
    |python                  |3.7.9      |  
    |pytorch                 |1.7.1      |
    |qt                      |5.9.7      |
    |sip                     |4.19.8     |
    |torchvision             |0.8.2      |      

- Download COCO database
    - Images
        1. [2017 Train images](http://images.cocodataset.org/zips/train2017.zip)
        1. [2017 Val images](http://images.cocodataset.org/zips/val2017.zip)
        1. [2017 Test images](http://images.cocodataset.org/zips/test2017.zip)
    
        *Extract the images directly to ```./data/coco/images```*
    
    - Annotations
        1. [2017 Train/Val annotations](http://images.cocodataset.org/annotations/annotations_trainval2017.zip)
        2. [2014 Train/Val annotations](http://images.cocodataset.org/annotations/annotations_trainval2014.zip)
        3. [2017 Testing Image info](http://images.cocodataset.org/annotations/image_info_test2017.zip)
        
        *Extract the json files directly to ```./data/coco/annotations```*

- Download trained model

| Image Size | Backbone      | FPS  | mAP  | Weights                                                                                                              |  |
|:----------:|:-------------:|:----:|:----:|----------------------------------------------------------------------------------------------------------------------|--------|
| 550        | Resnet50-FPN  | 42.5 | 28.2 | [yolact_resnet50_54_800000.pth](https://drive.google.com/file/d/1yp7ZbbDwvMiFJEq4ptVKTYTI2VeRDXl0/view?usp=sharing)  | [Mirror](https://ucdavis365-my.sharepoint.com/:u:/g/personal/yongjaelee_ucdavis_edu/EUVpxoSXaqNIlssoLKOEoCcB1m0RpzGq_Khp5n1VX3zcUw) |
| 550        | Darknet53-FPN | 40.0 | 28.7 | [yolact_darknet53_54_800000.pth](https://drive.google.com/file/d/1dukLrTzZQEuhzitGkHaGjphlmRJOjVnP/view?usp=sharing) | [Mirror](https://ucdavis365-my.sharepoint.com/:u:/g/personal/yongjaelee_ucdavis_edu/ERrao26c8llJn25dIyZPhwMBxUp2GdZTKIMUQA3t0djHLw)
| 550        | Resnet101-FPN | 33.5 | 29.8 | [yolact_base_54_800000.pth](https://drive.google.com/file/d/1UYy3dMapbH1BnmtZU4WH1zbYgOzzHHf_/view?usp=sharing)      | [Mirror](https://ucdavis365-my.sharepoint.com/:u:/g/personal/yongjaelee_ucdavis_edu/EYRWxBEoKU9DiblrWx2M89MBGFkVVB_drlRd_v5sdT3Hgg)
| 700        | Resnet101-FPN | 23.6 | 31.2 | [yolact_im700_54_800000.pth](https://drive.google.com/file/d/1lE4Lz5p25teiXV-6HdTiOJSnS7u7GBzg/view?usp=sharing)     | [Mirror](https://ucdavis365-my.sharepoint.com/:u:/g/personal/yongjaelee_ucdavis_edu/Eagg5RSc5hFEhp7sPtvLNyoBjhlf2feog7t8OQzHKKphjw)


## Run the App
Just run *yolact_app.py*
```shell
python yolact_app.py
```
