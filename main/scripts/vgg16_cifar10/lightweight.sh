python main/cifar10.py --arch vgg_16_bn --pretrain_dir checkpoint/cifar/cifar10/vgg_16_bn.pt --criterion Euclide_dis --compress_rate [0.05]*7+[0.2]*5 --shot 10
