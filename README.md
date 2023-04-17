# Élagage efficace des filtres basé sur les décompositions tensorielles

Nous présentons une nouvelle méthode d'élagage des filtres pour les réseaux de neurones, appelée CORING (pour effiCient tensOr decomposition-based filteR prunING en anglais). L'approche proposée maintient l'aspect multidimensionnel des filtres grâce à l'utilisation de décompositions tensorielles. Notre approche permet de mesurer la similarité entre les filtres de manière plus efficace et plus précise que les méthodes traditionnelles qui utilisent des versions vectorisées ou matricisées des filtres. Avec cette approche, nous pouvons effectuer l'élagage des filtres plus efficacement en gardant l'essentiel de l'information en utilisant des décompositions de tenseurs sur les filtres. Les expériences menées sur différentes architectures prouvent l'efficacité de CORING.

## Installation
1. OS: This repository is developed on Debian GNU/Linux 10. However, we tested it and it also runs well on Ubuntu 18.04 + or Windows 10+.
2. Main requirements:
    ```
    - python=3.9
    - pytorch 1.13
    - cuda 11.6
    - tensorly=0.7
    - numpy=1.21
    - thop 0.1
    - ptflops
    ```
3. Our environment may also be reproduced via conda:
    ```
    conda env create -f environment.yml
    ```
## Getting Started
1. Data preparation:
- The CIFAR-10 dataset is automatically downloaded to `./data/cifar10` when needed.
- Download the ImageNet dataset [4], put it to `./data/imagenet` and extract it. Instruction can be found on Github [5], for example:
    ```
    echo "Extract Train set of ImageNet"
    cd data/imagenet &&
    mkdir train && mv ILSVRC2012_img_train.tar train/ && cd train &&
    tar -xvf ILSVRC2012_img_train.tar && rm -f ILSVRC2012_img_train.tar
    find . -name "*.tar" | while read NAME ; do mkdir -p "${NAME%.tar}"; tar -xvf "${NAME}" -C "${NAME%.tar}"; rm -f "${NAME}"; done
    cd ..
    # val
    echo "Extract Val set of ImageNet"
    mkdir val && mv ILSVRC2012_img_val.tar val/ && mv valprep.sh val && cd val &&
    tar -xvf ILSVRC2012_img_val.tar &&
    cat valprep.sh | bash
    cd ..
    ```
2. Baseline models:
- Download baseline models [here](), put them to `./checkpoint`.

## Verification our results
- All results are available [here]().
- Log files of all experiments are attached, they contain all information of the pruning or fine tuning process, as well as model architecture, numbers of parameters/FLOPs and top-1/top-5 accuracy.
    | No | Dataset  |    Model    | Pruning level | Top-1 (%) | #Param. (↓%) |   FLOPs (↓%)  |
    |:--:|----------|:-----------:|:-------------:|:---------:|:------------:|:-------------:|
    |  1 | CIFAR-10 |  VGG-16-BN  |      soft     |   94.42   |  2.76M(81.6) | 131.17M(58.1) |
    |  2 | CIFAR-10 |  ResNet-56  |      soft     |   94.76   |  0.66M(22.4) |  91.23M(27.3) |
    |  3 | CIFAR-10 |   DenseNet  |      soft     |   94.88   |  0.80M(23.1) | 224.12M(20.8) |
    |  4 | CIFAR-10 | MobileNetv2 |    moderate   |   94.81   |  1.26M(43.8) |  55.16M(42.0) |
    |  6 | ImageNet |  Resnet-50  |    extreme    |   73.99   |  8.01M(68.6) |  0.95B(76.7)  |
    
    Model files are placed in `./pruned_model` and can be tested via the `main/test.py`.
    
    Please make sure to specify the appropriate dataset path, architecture, compression rate with corresponding model path.
    
    For example:
    ```
    python main/test.py --dataset cifar10 --data_dir data/cifar10 --arch vgg_16_bn --compress_rate [0.21]*7+[0.75]*5 --model_path ./pruned_model/cifar10/vgg16bn/soft/model_best.pth.tar
    python main/test.py --dataset cifar10 --data_dir data/cifar10 --arch resnet_56 --compress_rate [0.]+[0.18]*29 --model_path ./pruned_model/cifar10/resnet56/soft/model_best.pth.tar
    python main/test.py --dataset cifar10 --data_dir data/cifar10 --arch densenet_40 --compress_rate [0.]+[0.08]*6+[0.09]*6+[0.08]*26 --model_path ./pruned_model/cifar10/densenet/soft/model_best.pth.tar
    python main/test.py --dataset cifar10 --data_dir data/cifar10 --arch mobilenet_v2 --compress_rate [0.]+[0.1]+[0.25]*2+[0.25]*2+[0.3]*2 --model_path ./pruned_model/cifar10/mobilenetv2/moderate/model_best.pth.tar
    python main/test.py --dataset imagenet --data_dir data/imagenet --arch resnet_50 --compress_rate [0.]+[0.5]*3+[0.6]*16 --model_path ./pruned_model/imagenet/extreme/model_best.pth.tar
    ```
    
## Reproducibility and further developpement
1. To reproduce results, you may run prepared scripts.
- For CIFAR-10, the rank will be calculated during the pruning process.
- For Resnet50/ImageNet, first generate the rank by this:
    ```
    sh main/scripts/generate_rank_resnet50.sh
    ```
- Now, the pruning process can be performed via prepared scripts. For example:
    ```
    sh main/scripts/resnet50_imagenet/vbd.sh
    ```
2. Our code is pipelined and can be integrated in other works. Just replace the filter ranking computation.
    ```
    # replace your rank calculation here
    rank = get_rank(oriweight, args.criterion, args.strategy)
    ```

## Acknowledgement
Part of this repository is based on HRank [1] which is kindly cited in the paper.

## References
[1]: Mingbao Lin et al. Hrank: Filter pruning using high-rank feature map. CVPR  2020.

[2]: Yang Sui et al. Chip: Channel independence-based pruning for compact neural networks. NeurIPS 2021.

[3]: Thibault Castells and Seul-Ki Yeom. Automatic neural network pruning that efficiently preserves the model accuracy. AAAI 2023.

[4]: The ImageNet dataset: https://image-net.org/download-images.php

[5]: Duong H. Le and Binh-Son Hua. Network Pruning That Matters: A Case Study on Retraining Variants. ICLR 2021.
