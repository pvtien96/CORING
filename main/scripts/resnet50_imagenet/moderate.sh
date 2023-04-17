python main/imagenet.py --arch resnet_50 --use_pretrain --pretrain_dir checkpoint/imagenet/resnet_50.pth --criterion VBD_dis --compress_rate [0.]+[0.12]*3+[0.38]*16
