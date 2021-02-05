# YOLACT-GUI

---

A GUI for YOLACT.

**[Original repo](https://github.com/dbolya/yolact)**

## Installation
- Clone this repo and enter it
    ```Shell
    git clone https://github.com/jiancong0204/yolact-gui
    cd yolact-gui
    mkdir -p data/coco/images
    mkdir -p data/coco/annotations
    mkdir weights
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
    
## Run the App
Just run *yolact_app.py*
```shell
python yolact_app.py
```
