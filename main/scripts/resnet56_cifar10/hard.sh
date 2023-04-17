python main/cifar10.py --arch resnet_56 --pretrain_dir checkpoint/cifar/cifar10/resnet_56.pt --criterion Euclide_dis --compress_rate [0.]+[0.4]*2+[0.5]*9+[0.6]*9+[0.7]*9 --shot 1
