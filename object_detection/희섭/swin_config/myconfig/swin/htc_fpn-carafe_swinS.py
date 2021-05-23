"""
swin small + fpn-carafe + htc default 모델 조합
(기본 설정에 instaboost, multiscaling등의 기준을 추가)
"""
_base_ = [
    '../_base_/models/htc_swin_fpn-carafe.py',
    '../_base_/datasets/coco_instance-Aug2.py',
    '../_base_/schedules/schedule_tun.py', '../_base_/default_runtime.py'
]

model = dict(
    backbone=dict(
        embed_dim=96,
        depths=[2, 2, 18, 2],
        num_heads=[3, 6, 12, 24],
        window_size=7,
        ape=False,
        drop_path_rate=0.2,
        patch_norm=True,
        use_checkpoint=False
    ),
    neck=dict(in_channels=[96, 192, 384, 768]),
)

# img_norm_cfg = dict(
#     mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)


# """ Augmentation """
# albu_train_transforms = [
#     dict(
#         type='Rotate',
#         limit=8,
#         border_mode=0,
#         p=0.8
#     ),
#     dict(
#         type='RandomSizedBBoxSafeCrop',
#         height=512,
#         width=512,
#         erosion_rate=0.2,
#         p=0.8
#     ),
#     dict(
#         type='CLAHE',
#         clip_limit=(1.5, 4.0),
#         p=0.8
#     ),
# ]
# albu_test_transforms = [
#     dict(
#         type='CLAHE',
#         clip_limit=(1.5, 4.0),
#         p=1.0,
#         # clip_limit=(1.1, 3.0),
#         # p=0.95,
#         always_apply=True
#     ),
# ]

# """ Pipelines """
# train_pipeline = [
#     dict(type='LoadImageFromFile'),
#     dict(type='LoadAnnotations', with_bbox=True, with_label=True, with_mask=True),
#     dict(type='Resize',
#          img_scale=[(448, 512), (480, 512), (512, 512), (544, 512), (576, 512),
#                      (608, 512), (640, 512), (672, 512), (704, 512),
#                      (736, 512), (768, 512), (800, 512)],
#          multiscale_mode='value',
#          keep_ratio=True),
#     dict(type='RandomFlip', flip_ratio=[0.5, 0.1], direction=['horizontal', 'vertical']),
#     dict(
#         type='Albu',
#         transforms=albu_train_transforms,
#         bbox_params=dict(
#             type='BboxParams',
#             format='pascal_voc',
#             label_fields=['gt_labels'],
#             min_area=3**2,
#             min_visibility=0.2,
#             # A simple workaround to remove masks without boxes
#             filter_lost_elements=True),
#         keymap={
#             'img': 'image',
#             'gt_bboxes': 'bboxes',
#             'gt_masks': 'masks'
#         },
#         # update final shape
#         update_pad_shape=False,
#         # skip_img_without_anno(bool): Whether to skip the image if no ann left after aug
#         skip_img_without_anno=True
#     ),
    
#     dict(type='Normalize', **img_norm_cfg),
#     # dict(type='Pad', size_divisor=32),
#     dict(type='DefaultFormatBundle'),
#     dict(
#         type='Collect',
#         keys=['img', 'gt_bboxes', 'gt_labels', 'gt_masks'],
#         meta_keys=('filename', 'ori_shape', 'img_shape', 'img_norm_cfg', 'pad_shape', 'scale_factor')
#     )
# ]

# test_pipeline = [
#     dict(type='LoadImageFromFile'),
#     dict(
#         type='Albu',
#         transforms=albu_test_transforms,
#         bbox_params=dict(
#             type='BboxParams',
#             format='pascal_voc'
#         ),
#         keymap={
#             'img': 'image',
#             # 'gt_bboxes': 'bboxes',
#             # 'gt_masks': 'masks'
#         },
#         # update final shape
#         update_pad_shape=False,
#         # skip_img_without_anno(bool): Whether to skip the image if no ann left after aug
#         skip_img_without_anno=True
#     ),
#     dict(
#         type='MultiScaleFlipAug',
#         img_scale=[(512, 512)],
#         flip=True,
#         transforms=[
#             dict(type='Resize', keep_ratio=True),
#             dict(type='RandomFlip', flip_ratio=0.5, direction='horizontal'),
#             dict(type='Normalize', **img_norm_cfg),
#             dict(type='DefaultFormatBundle'),
#             dict(type='Collect', keys=['img']),
#         ]
#     )
# ]

# data = dict(train=dict(pipeline=train_pipeline),
#             val=dict(pipeline=test_pipeline),
#             test=dict(pipeline=test_pipeline))


# swin default scheduler
optimizer = dict(_delete_=True, type='AdamW', lr=0.0001, betas=(0.9, 0.999), weight_decay=0.05,
                 paramwise_cfg=dict(custom_keys={'absolute_pos_embed': dict(decay_mult=0.),
                                                 'relative_position_bias_table': dict(decay_mult=0.),
                                                 'norm': dict(decay_mult=0.)}))

runner = dict(type='EpochBasedRunner', max_epochs=36) #apex 안쓸때



load_from = "/opt/ml/model/cascade_mask_rcnn_swin_small_patch4_window7.pth"

