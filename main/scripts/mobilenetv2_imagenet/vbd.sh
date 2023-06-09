#round 1
for cpr in [0.]+[0.12]+[0.25]*2+[0.36]*2+[0.4]*2
do
   python main/evaluate.py --arch mobilenet_v2 --job_dir round1 --use_pretrain --pretrain_dir checkpoint/imagenet/mobilenet_v2.pt --criterion VBD_dis --strategy min_sum --compress_rate $cpr --epochs 200 --weight_decay 0.00004 --batch_size 256
done
