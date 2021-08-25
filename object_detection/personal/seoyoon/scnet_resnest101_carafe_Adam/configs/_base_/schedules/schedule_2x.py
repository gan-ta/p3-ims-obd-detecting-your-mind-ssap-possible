# optimizer
# optimizer = dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0001)
# optimizer = dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0001)   #for yolof

optimizer = dict(type='Adam', lr=5e-5, weight_decay= 1e-6)
#optimizer = dict(type='AdamW', lr=5e-5, weight_decay= 1e-6)
optimizer_config = dict(grad_clip=None)
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.001,
    step=[16, 22])

# lr_config = dict(
#     policy='CosineAnnealing',
#     warmup='linear',
#     warmup_iters=1000,
#     warmup_ratio=1.0 / 10,
#     min_lr_ratio=1e-5)

runner = dict(type='EpochBasedRunner', max_epochs=72)
# evaluation = dict(interval=1, metric='bbox', save_best="bbox_mAP")