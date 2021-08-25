import os


""" Configurations """
# Paths
data_dir = r'/opt/ml/input/data/'
# Dataset
dataset_type = 'CocoDataset'
classes = (
    "UNKNOWN", "General trash", "Paper", "Paper pack", "Metal",
    "Glass", "Plastic", "Styrofoam", "Plastic bag", "Battery",
    "Clothing"
)
# Normalization
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    to_rgb=True
)

""" Pipelines """
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', img_scale=(512, 512), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(512, 512),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip', flip_ratio=0.5),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='DefaultFormatBundle'),
            # dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]

""" Dataset """
data = dict(
    samples_per_gpu=4,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        classes=classes,
        ann_file=os.path.join(data_dir, r'train.json'),
        img_prefix=data_dir,
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        classes=classes,
        ann_file=os.path.join(data_dir, r'val.json'),
        img_prefix=data_dir,
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        classes=classes,
        ann_file=os.path.join(data_dir, r'test.json'),
        img_prefix=data_dir,
        pipeline=test_pipeline))
