import os
import os.path as osp
import numpy as np
import datetime
import argparse
import copy
from collections import OrderedDict
from tqdm.auto import tqdm

import torch
import torch.nn as nn
import torch.utils
import torch.backends.cudnn as cudnn
import torch.utils.data.distributed

from models.cifar10.vgg import vgg_16_bn
from models.cifar10.resnet import resnet_56, resnet_110
from models.cifar10.googlenet import googlenet, Inception
from models.cifar10.densenet import densenet_40

import utils.common as utils

import sys
sys.path.append(os.path.dirname('..'))
from similarity import similarity
from calculation.ranking_strategy import get_saliency
from calculation.decompose import decompose


parser = argparse.ArgumentParser("Rank generation")
parser.add_argument(
    '--arch',
    type=str,
    default='resnet_56',
    help='architecture')
parser.add_argument(
    '--job_dir',
    type=str,
    default='resnet/result/hrankplus/resnet_56/standard',
    help='path for saving trained models')
parser.add_argument(
    '--pretrain_dir',
    type=str,
    default='./resnet/checkpoint/cifar/cifar10/resnet_56.pt',
    help='pretrain model path')
parser.add_argument(
    '--rank_conv_prefix',
    type=str,
    default='./resnet/hosvd_rank_conv/',
    help='rank conv file folder')
parser.add_argument(
    '--gpu',
    type=str,
    default='0',
    help='Select gpu to use')
parser.add_argument(
    '--resume',
    action='store_true',
    help='whether continue training from the same directory')
parser.add_argument(
    '--criterion',
    default='VBD_dis',
    type=str,
    help='criterion')
parser.add_argument(
    '--strategy',
    default='min_sum',
    type=str,
    help='strategy')

args = parser.parse_args()

os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

if not osp.isdir(args.job_dir):
    os.makedirs(args.job_dir)

utils.record_config(args)
now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
logger = utils.get_logger(osp.join(args.job_dir, 'gen_rank_'+now+'.log'))

# use for loading pretrain model
if len(args.gpu) > 1:
    name_base = 'module.'
else:
    name_base = ''

# creat folder to save rank files
prefix = osp.join(args.rank_conv_prefix, args.arch,
                    args.strategy, args.criterion,
                    'rank_conv')
if not osp.isdir(prefix):
    os.makedirs(prefix)
subfix = ".npy"


def get_correlation_mat(all_filters_u_dict):
    """Caculate correlation matrix between channels in inter-layer
        based on precalculated left-singular vectors dict of hosvd
    """
    num_filters = len(all_filters_u_dict)
    correlation_mat = [[0.]*num_filters for i in range(num_filters)]

    # compute the channel pairwise similarity based on criterion VBD_dis
    for i in tqdm(range(num_filters)):
        for j in range(num_filters):
            ui = all_filters_u_dict[i]
            uj = all_filters_u_dict[j]
            sum = 0.
            for x in range(3):
                sum += similarity(torch.tensor(ui[x]),
                                  torch.tensor(uj[x]),
                                  criterion=args.criterion
                                  )
            correlation_mat[i][j] = (sum/3).item()

    return correlation_mat


def get_rank(weight):
    """Get rank based on HOSVD+VBD+min_sum"""
    num_filters = weight.shape[1]
    all_filters_u_dict = {}
    for i_filter in range(num_filters):
        filter = weight.detach()[:, i_filter]
        u = decompose(filter, decomposer='hosvd')
        all_filters_u_dict[i_filter] = [i.tolist() for i in u]

    correl_matrix = get_correlation_mat(all_filters_u_dict)
    correl_matrix = np.array(correl_matrix)

    dis = 1 if 'dis' in args.criterion else -1
    saliency = get_saliency(correl_matrix, args.strategy, dis)

    return saliency


def save(rank, cov_id):
    save_pth = prefix + str(cov_id) + subfix
    logger.info('saving rank to: ' + save_pth)
    np.save(save_pth, rank)


def rank_vgg(model, state_dict):
    # iterate over all convolutional layers
    cnt = 0
    for name, module in model.named_modules():
        name = name.replace('module.', '')
        if isinstance(module, nn.Conv2d):
            cnt += 1
            weight = state_dict[name + '.weight']
            cov_id = cnt
            rank = get_rank(weight)
            save(rank, cov_id)


def rank_resnet(state_dict, layer):
    cfg = {
        56: [9, 9, 9],
        110: [18, 18, 18],
    }

    current_cfg = cfg[layer]

    # iterate over all convolutional layers
    cnt = 1
    for layer, num in enumerate(current_cfg):
        layer_name = 'layer' + str(layer + 1) + '.'
        print(f"layer_name = {layer_name}, num = {num}")
        for k in range(num):
            for l in range(2):
                cnt += 1
                cov_id = cnt

                conv_name = layer_name + str(k) + '.conv' + str(l + 1)
                print(f"conv_name = {conv_name}")
                conv_weight_name = conv_name + '.weight'
                weight = state_dict[conv_weight_name]
                rank = get_rank(weight)
                save(rank, cov_id)


def load_google_model(model, oristate_dict):
    state_dict = model.state_dict()

    filters = [
        [64, 128, 32, 32],
        [128, 192, 96, 64],
        [192, 208, 48, 64],
        [160, 224, 64, 64],
        [128, 256, 64, 64],
        [112, 288, 64, 64],
        [256, 320, 128, 128],
        [256, 320, 128, 128],
        [384, 384, 128, 128]
    ]

    # last_select_index = []
    all_honey_conv_name = []
    all_honey_bn_name = []
    cur_last_select_index = []

    cnt = 0
    for name, module in model.named_modules():
        name = name.replace('module.', '')

        if isinstance(module, Inception):

            cnt += 1
            cov_id = cnt

            honey_filter_channel_index = [
                '.branch5x5.6',
            ]  # the index of sketch filter and channel weight
            honey_channel_index = [
                '.branch1x1.0',
                '.branch3x3.0',
                '.branch5x5.0',
                '.branch_pool.1'
            ]  # the index of sketch channel weight
            honey_filter_index = [
                '.branch3x3.3',
                '.branch5x5.3',
            ]  # the index of sketch filter weight
            honey_bn_index = [
                '.branch3x3.4',
                '.branch5x5.4',
                '.branch5x5.7',
            ]  # the index of sketch bn weight

            for bn_index in honey_bn_index:
                all_honey_bn_name.append(name + bn_index)

            last_select_index = cur_last_select_index[:]
            cur_last_select_index = []

            for weight_index in honey_channel_index:

                if '3x3' in weight_index:
                    branch_name = '_n3x3'
                elif '5x5' in weight_index:
                    branch_name = '_n5x5'
                elif '1x1' in weight_index:
                    branch_name = '_n1x1'
                elif 'pool' in weight_index:
                    branch_name = '_pool_planes'

                conv_name = name + weight_index + '.weight'
                all_honey_conv_name.append(name + weight_index)

                oriweight = oristate_dict[conv_name]
                curweight = state_dict[name_base+conv_name]
                orifilter_num = oriweight.size(1)
                currentfilter_num = curweight.size(1)

                if orifilter_num != currentfilter_num:
                    select_index = last_select_index
                else:
                    select_index = list(range(0, orifilter_num))

                for i in range(state_dict[name_base+conv_name].size(0)):
                    for index_j, j in enumerate(select_index):
                        state_dict[name_base+conv_name][i][index_j] = \
                            oristate_dict[conv_name][i][j]

                if branch_name == '_n1x1':
                    tmp_select_index = list(
                        range(state_dict[name_base+conv_name].size(0)))
                    cur_last_select_index += tmp_select_index
                if branch_name == '_pool_planes':
                    tmp_select_index = list(
                        range(state_dict[name_base+conv_name].size(0)))
                    tmp_select_index = [x+filters[cov_id-2][0]+filters[cov_id-2]
                                        [1]+filters[cov_id-2][2] for x in tmp_select_index]
                    cur_last_select_index += tmp_select_index

            for weight_index in honey_filter_index:

                if '3x3' in weight_index:
                    branch_name = '_n3x3'
                elif '5x5' in weight_index:
                    branch_name = '_n5x5'
                elif '1x1' in weight_index:
                    branch_name = '_n1x1'
                elif 'pool' in weight_index:
                    branch_name = '_pool_planes'

                conv_name = name + weight_index + '.weight'

                all_honey_conv_name.append(name + weight_index)
                oriweight = oristate_dict[conv_name]
                curweight = state_dict[name_base+conv_name]

                orifilter_num = oriweight.size(0)
                currentfilter_num = curweight.size(0)

                if orifilter_num != currentfilter_num:
                    logger.info('loading rank from: ' + prefix +
                                str(cov_id) + branch_name + subfix)
                    rank = np.load(prefix + str(cov_id) + branch_name + subfix)
                    if args.random_rank:
                        rank = np.random.random_sample(rank.shape)
                    select_index = np.argsort(
                        rank)[orifilter_num - currentfilter_num:]  # preserved filter id
                    select_index.sort()
                else:
                    select_index = list(range(0, orifilter_num))

                for index_i, i in enumerate(select_index):
                    state_dict[name_base+conv_name][index_i] = \
                        oristate_dict[conv_name][i]

                if branch_name == '_n3x3':
                    tmp_select_index = [x+filters[cov_id-2][0]
                                        for x in select_index]
                    cur_last_select_index += tmp_select_index
                if branch_name == '_n5x5':
                    last_select_index = select_index

            for weight_index in honey_filter_channel_index:

                if '3x3' in weight_index:
                    branch_name = '_n3x3'
                elif '5x5' in weight_index:
                    branch_name = '_n5x5'
                elif '1x1' in weight_index:
                    branch_name = '_n1x1'
                elif 'pool' in weight_index:
                    branch_name = '_pool_planes'

                conv_name = name + weight_index + '.weight'
                all_honey_conv_name.append(name + weight_index)

                oriweight = oristate_dict[conv_name]
                curweight = state_dict[name_base+conv_name]

                orifilter_num = oriweight.size(1)
                currentfilter_num = curweight.size(1)

                if orifilter_num != currentfilter_num:
                    select_index = last_select_index
                else:
                    select_index = range(0, orifilter_num)

                orifilter_num = oriweight.size(0)
                currentfilter_num = curweight.size(0)

                select_index_1 = copy.deepcopy(select_index)

                if orifilter_num != currentfilter_num:
                    logger.info('loading rank from: ' + prefix +
                                str(cov_id) + branch_name + subfix)
                    rank = np.load(prefix + str(cov_id) + branch_name + subfix)
                    if args.random_rank:
                        rank = np.random.random_sample(rank.shape)
                    select_index = np.argsort(
                        rank)[orifilter_num - currentfilter_num:]  # preserved filter id
                    select_index.sort()

                else:
                    select_index = list(range(0, orifilter_num))

                if branch_name == '_n5x5':
                    tmp_select_index = [x+filters[cov_id-2][0] +
                                        filters[cov_id-2][1] for x in select_index]
                    cur_last_select_index += tmp_select_index

                for index_i, i in enumerate(select_index):
                    for index_j, j in enumerate(select_index_1):
                        state_dict[name_base+conv_name][index_i][index_j] = \
                            oristate_dict[conv_name][i][j]

        elif name == 'pre_layers':

            cnt += 1
            cov_id = cnt

            honey_filter_index = ['.0']  # the index of sketch filter weight
            honey_bn_index = ['.1']  # the index of sketch bn weight

            for bn_index in honey_bn_index:
                all_honey_bn_name.append(name + bn_index)

            for weight_index in honey_filter_index:

                conv_name = name + weight_index + '.weight'

                all_honey_conv_name.append(name + weight_index)
                oriweight = oristate_dict[conv_name]
                curweight = state_dict[name_base+conv_name]

                orifilter_num = oriweight.size(0)
                currentfilter_num = curweight.size(0)

                if orifilter_num != currentfilter_num:
                    rank = np.load(prefix + str(cov_id) + subfix)
                    if args.random_rank:
                        rank = np.random.random_sample(rank.shape)
                    select_index = np.argsort(
                        rank)[orifilter_num - currentfilter_num:]  # preserved filter id
                    select_index.sort()

                    cur_last_select_index = select_index[:]

                    for index_i, i in enumerate(select_index):
                        state_dict[name_base+conv_name][index_i] = \
                            oristate_dict[conv_name][i]  # '''

    for name, module in model.named_modules():  # Reassign non sketch weights to the new network
        name = name.replace('module.', '')

        if isinstance(module, nn.Conv2d):
            if name not in all_honey_conv_name:
                state_dict[name_base+name +
                           '.weight'] = oristate_dict[name + '.weight']
                state_dict[name_base+name +
                           '.bias'] = oristate_dict[name + '.bias']

        elif isinstance(module, nn.BatchNorm2d):

            if name not in all_honey_bn_name:
                state_dict[name_base+name +
                           '.weight'] = oristate_dict[name + '.weight']
                state_dict[name_base+name +
                           '.bias'] = oristate_dict[name + '.bias']
                state_dict[name_base+name +
                           '.running_mean'] = oristate_dict[name + '.running_mean']
                state_dict[name_base+name +
                           '.running_var'] = oristate_dict[name + '.running_var']

        elif isinstance(module, nn.Linear):
            state_dict[name_base+name +
                       '.weight'] = oristate_dict[name + '.weight']
            state_dict[name_base+name +
                       '.bias'] = oristate_dict[name + '.bias']

    model.load_state_dict(state_dict)


def load_densenet_model(model, oristate_dict):

    state_dict = model.state_dict()
    last_select_index = []  # Conv index selected in the previous layer

    cnt = 0
    prefix = osp.join(args.rank_conv_prefix, args.arch, 'rank_conv')
    subfix = ".npy"
    for name, module in model.named_modules():
        name = name.replace('module.', '')

        if isinstance(module, nn.Conv2d):

            cnt += 1
            cov_id = cnt
            oriweight = oristate_dict[name + '.weight']
            curweight = state_dict[name_base+name + '.weight']
            orifilter_num = oriweight.size(0)
            currentfilter_num = curweight.size(0)

            if orifilter_num != currentfilter_num:
                logger.info('loading rank from: ' +
                            prefix + str(cov_id) + subfix)
                rank = np.load(prefix + str(cov_id) + subfix)
                if args.random_rank:
                    rank = np.random.random_sample(rank.shape)
                # preserved filter id
                select_index = list(np.argsort(
                    rank)[orifilter_num-currentfilter_num:])
                select_index.sort()

                if last_select_index is not None:
                    for index_i, i in enumerate(select_index):
                        for index_j, j in enumerate(last_select_index):
                            state_dict[name_base+name + '.weight'][index_i][index_j] = \
                                oristate_dict[name + '.weight'][i][j]
                else:
                    for index_i, i in enumerate(select_index):
                        state_dict[name_base+name + '.weight'][index_i] = \
                            oristate_dict[name + '.weight'][i]

            elif last_select_index is not None:
                for i in range(orifilter_num):
                    for index_j, j in enumerate(last_select_index):
                        state_dict[name_base+name + '.weight'][i][index_j] = \
                            oristate_dict[name + '.weight'][i][j]
                select_index = list(range(0, orifilter_num))

            else:
                select_index = list(range(0, orifilter_num))
                state_dict[name_base+name + '.weight'] = oriweight

            if cov_id == 1 or cov_id == 14 or cov_id == 27:
                last_select_index = select_index
            else:
                tmp_select_index = [x+cov_id*12 -
                                    (cov_id-1)//13*12 for x in select_index]
                last_select_index += tmp_select_index

    model.load_state_dict(state_dict)


def main():
    cudnn.benchmark = True
    cudnn.enabled = True
    logger.info("args = %s", args)

    logger.info(f'Loading pretrain model: {args.pretrain_dir}')
    model = eval(args.arch)(compress_rate=[0.] * 100).cuda()
    ckpt = torch.load(args.pretrain_dir, map_location='cuda:0')

    if args.arch == 'densenet_40' or args.arch == 'resnet_110':
        new_state_dict = OrderedDict()
        for k, v in ckpt['state_dict'].items():
            new_state_dict[k.replace('module.', '')] = v
        model.load_state_dict(new_state_dict)
    else:
        model.load_state_dict(ckpt['state_dict'], strict=False)

    state_dict = model.state_dict()

    if args.arch == 'googlenet':
        load_google_model(model, state_dict)
    elif args.arch == 'vgg_16_bn':
        rank_vgg(model, state_dict)
    elif args.arch == 'resnet_56':
        rank_resnet(state_dict, 56)
    elif args.arch == 'resnet_110':
        rank_resnet(state_dict, 110)
    elif args.arch == 'densenet_40':
        load_densenet_model(model, state_dict)
    else:
        raise ValueError("Not implemented arch")


if __name__ == '__main__':
    main()
