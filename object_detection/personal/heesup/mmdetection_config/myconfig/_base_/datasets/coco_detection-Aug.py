"""
detection model + Augmentation 적용 및 튜닝을 한 dataset 
(faster rcnn으로 Augmentation 실험 시 사용)
"""
dataset_type = 'CocoDataset'
data_root = 'data/coco/'

albu_train_transforms = [
    
    dict(
        type='RandomBrightnessContrast',
        brightness_limit=[0.1, 0.3],
        contrast_limit=[0.1, 0.3],
        p=0.5),
#      dict(type='Blur', blur_limit=3, p=0.5),
    
#      dict(type='RandomSizedCrop', width = 256, height = 256, p=0.5),

#      dict(type='RandomSizedBBoxSafeCrop', width = 256, height = 256, p=0.5),
#     dict(
#         type = "RandomSizedBBoxSafeCrop",
#         width = 448,
#         height = 336,
#         erosion_rate=0.2
#     )
#     dict(
#         type = "OneOf",
#         transforms=[
#             dict(type = "HorizontalFlip",p = 1.0),
#             dict(type = "CLAHE",clip_limit = 3.0,p=1.0),
#             dict(type = "Rotate",limit = 30,p = 1.0)
#         ], p = 0.5
#     )
#       dict(type = "CLAHE",clip_limit = 3.0,p=0.5),
#     dict(
#         type='ShiftScaleRotate',
#         shift_limit=0.0625,
#         scale_limit=0.0,
#         rotate_limit=0,
#         interpolation=1,
#         p=0.5),
#     dict(
#         type='Cutout',
#         num_holes=10,
#         max_h_size=30,
#         max_w_size=30,
#         p=0.5)
]

img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', img_scale=(1333, 800), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(
        type='Albu',
        transforms=albu_train_transforms,
        bbox_params=dict(
            type='BboxParams',
            format='pascal_voc',
            label_fields=['gt_labels'],
            min_visibility=0.3,
            filter_lost_elements=True),
        keymap={
            'img': 'image',
            'gt_masks': 'masks',
            'gt_bboxes': 'bboxes'
        },
        update_pad_shape=False,
        skip_img_without_anno=True),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1333, 800),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=2, # 배치 사이즈
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_train2017.json',
        img_prefix=data_root + 'train2017/',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_val2017.json',
        img_prefix=data_root + 'val2017/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_val2017.json',
        img_prefix=data_root + 'val2017/',
        pipeline=test_pipeline))
evaluation = dict(interval=1, metric='bbox',save_best="bbox_mAP_50")
