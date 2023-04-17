python main/cifar10.py --arch densenet_40 --pretrain_dir checkpoint/cifar/cifar10/densenet_40.pt --criterion cosine_sim --compress_rate [0.]+[0.08]*6+[0.09]*6+[0.08]*26 --shot 1
