# encoding: utf-8
"""
@author:  wuxin.wang
@contact: wuxin.wang@whu.edu.cn
"""

import torch
from .swa import SWA

def make_optimizer(cfg, model):
    param_optimizer = list(model.named_parameters())
    no_decay = ['bias', 'bn']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': cfg.SOLVER.WEIGHT_DECAY},
        {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]

    optimizer = getattr(torch.optim, cfg.SOLVER.OPTIMIZER_NAME)(model.parameters(), lr=cfg.SOLVER.BASE_LR, momentum=cfg.SOLVER.MOMENTUM, nesterov=True)
    opt = SWA(optimizer, swa_start=10, swa_freq=5, swa_lr=None)
    return optimizer