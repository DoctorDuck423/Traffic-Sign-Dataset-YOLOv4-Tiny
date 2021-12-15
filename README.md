# Traffic-Sign-Dataset-YOLOv4-Tiny

Clone the github repository: `git clone https://github.com/AlexeyAB/darknet` on Linux(terminal) or Windows(Powershell).

### Compile the github repository(on Windows) 

```PowerShell
git clone https://github.com/AlexeyAB/darknet
cd darknet
./build.ps1 -UseVCPKG -EnableOPENCV -EnableCUDA -EnableCUDNN -EnableOPENCV_CUDA
```
### Compile the github repository (on Linux)

First edit the makefile inside the darknet folder and change the parameters (if neccesary) that are mentioned below.  

- `GPU=1` to build with CUDA to accelerate by using GPU (CUDA should be in `/usr/local/cuda`)
- `CUDNN=1` to build with cuDNN v5-v7 to accelerate training by using GPU (cuDNN should be in `/usr/local/cudnn`)
- `CUDNN_HALF=1` to build for Tensor Cores (on Titan V / Tesla V100 / DGX-2 and later) speedup Detection 3x, Training 2x
- `OPENCV=1` to build with OpenCV 4.x/3.x/2.4.x - allows to detect on video files and video streams from network cameras or web-cams
- `DEBUG=0` to build debug version of Yolo
- `OPENMP=1` to build with OpenMP support to accelerate Yolo by using multi-core CPU
- `LIBSO=0` to build a library `darknet.so` and binary runnable file `uselib` that uses this library. Or you can try to run so `LD_LIBRARY_PATH=./:$LD_LIBRARY_PATH ./uselib test.mp4` How to use this SO-library from your own code - you can look at C++ example: https://github.com/AlexeyAB/darknet/blob/master/src/yolo_console_dll.cpp
    or use in such a way: `LD_LIBRARY_PATH=./:$LD_LIBRARY_PATH ./uselib data/coco.names cfg/yolov4.cfg yolov4.weights test.mp4`
- `ZED_CAMERA=1` to build a library with ZED-3D-camera support (should be ZED SDK installed), then run
    `LD_LIBRARY_PATH=./:$LD_LIBRARY_PATH ./uselib data/coco.names cfg/yolov4.cfg yolov4.weights zed_camera`
- You also need to specify for which graphics card the code is generated. This is done by setting `ARCH=`. If you use a never version than CUDA 11 you further need to edit line 20 from Makefile and remove `-gencode arch=compute_30,code=sm_30 \` as Kepler GPU support was dropped in CUDA 11. You can also drop the general `ARCH=` and just uncomment `ARCH=` for your graphics card.

```PowerShell
git clone https://github.com/AlexeyAB/darknet
cd darknet
make
```

### Create/Edit Dataset

This dataset is located in `darknet/data/obj` and all images contain a text file: For example `img1.jpg` has `img1.txt`, this text files contains the boundaries of the object that we want to detect. 

The boundaries(example)= `26 0.504178 0.408115 0.206128 0.443914` where `26` is the object number corresponding to "Speed Sign 65"

To add new objects then you need to start with object number `27`

To locate this boundaries you can use a software called LabelIMg link:https://tzutalin.github.io/labelImg/ or any other software that can make boundaries of the object in YOLO format. 

### Set training files 

There are two files in `darknet/data` that are `obj.name` and `obj.data`. The first file contains all objects in order that were used for training that are in conjuction with the object number in the dataset text files. For example `0` represents the object `Stop` and `1` represents `Yield`, and it continues until `Speed Limit 85`. If a new object is added in the dataset then a new object name must be added in `obj.name`

`obj.data` contains the number of objects `classes = 32 `, change the number if adding or removing classes. 
`train  = data/train.txt`, the text file that contains the path to the text files that are going to be used for training.
`valid  = data/test.txt`, the text file that contains the path to the text files that are going to be used for validation.
`names = data/obj.names`, tell trhe training proccess which object number has a name.   
`backup = backup/`, where the training output (weights) will be saved !If no folder then it will not work, create folder if neccesary. 

To create the `train.txt` and `test.tx` run the the script `proccess.py` and that should split the images for training and validation. 

```PowerShell
cd data
python process.py
```

### Edit Configuration file 

Edit the configuration file `cfg/yolov4-tiny-custom-traffic` 

- change line batch to [`batch=64`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L3)
- change line subdivisions to [`subdivisions=16`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L4)
- change line max_batches to (`classes*2000`, but not less than number of training images and not less than `6000`), f.e. [`max_batches=6000`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L20) if you train for 3 classes
- change line steps to 80% and 90% of max_batches, f.e. [`steps=4800,5400`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L22)
- set network size `width=416 height=416` or any value multiple of 32: https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L8-L9
- change line `classes=80` to your number of objects in each of 3 `[yolo]`-layers:
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L610
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L696
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L783
- change [`filters=255`] to filters=(classes + 5)x3 in the 3 `[convolutional]` before each `[yolo]` layer, keep in mind that it only has to be the last `[convolutional]` before each of the `[yolo]` layers.
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L603
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L689
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L776

So if `classes=1` then should be `filters=18`. If `classes=2` then write `filters=21`.
**(Do not write in the cfg-file: filters=(classes + 5)x3)**

(Generally `filters` depends on the `classes`, `coords` and number of `mask`s, i.e. filters=`(classes + coords + 1)*<number of mask>`, where `mask` is indices of anchors. If `mask` is absence, then filters=`(classes + coords + 1)*num`)

So for example, for 2 objects, your file `yolo-obj.cfg` should differ from `yolov4-custom.cfg` in such lines in each of **3** [yolo]-layers:

```ini
[convolutional]
filters=21

[region]
classes=2
```

### Run the training

Because we are using Yolov4-tiny for training the we used a pretrained weight `yolov4-tiny.conv.29` which can be downloaded from https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29

To run the training, run this command `./darknet detector train data/obj.data cfg/yolov4-tiny-custom-traffic.cfg yolov4-tiny.conv.29 -map` 

Wait some hours or until the mAP reaches a desirable number and the average error is less than 3 percent. 

During these hours, some weights will be saved in `backup/` based on the number of iterations.

### Validate the training 

To validate the weights run this command `./darknet detector test data/obj.data cfg/yolov4-tiny-custom-traffic.cfg backup/yolov4-tiny-custom-traffic_last.weights` and change `yolov4-tiny-custom-traffic_last.weights` for the desirable weight to use. 

You can also use it on video for validation with this command `./darknet detector demo data/obj.data cfg/yolov4-tiny-custom-traffic.cfg backup/yolov4-tiny-custom-traffic_last.weights -ext_output data/stop_video.mp4` where `data/stop_video.mp4` can be change with any video. 

Or a camera input video with this command `./darknet detector demo data/obj.data cfg/yolov4-tiny-custom-traffic.cfg backup/yolov4-tiny-custom-traffic_last.weights -c 0`






 



