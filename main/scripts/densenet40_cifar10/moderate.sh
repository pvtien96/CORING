python main/cifar10.py --arch densenet_40 --pretrain_dir checkpoint/cifar/cifar10/densenet_40.pt --criterion Euclide_dis --compress_rate [0.]+[0.2]*12+[0.]+[0.2]*12+[0.]+[0.2]*12 --shot 1
