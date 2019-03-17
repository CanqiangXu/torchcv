#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Donny You(youansheng@gmail.com)
# Some methods used by main methods.


import os

from utils.helpers.file_helper import FileHelper
from utils.tools.logger import Logger as Log


class Controller(object):

    @staticmethod
    def init(runner):
        runner.runner_state['iters'] = 0
        runner.runner_state['last_iters'] = 0
        runner.runner_state['epoch'] = 0
        runner.runner_state['last_epoch'] = 0
        runner.runner_state['performance'] = 0
        runner.runner_state['val_loss'] = 0
        runner.runner_state['max_performance'] = 0
        runner.runner_state['min_val_loss'] = 0

    @staticmethod
    def train(runner):
        Log.info('Training start...')
        if runner.configer.get('network', 'resume') is not None and runner.configer.get('network', 'resume_val'):
            runner.val()

        if runner.configer.get('solver', 'lr')['metric'] == 'epoch':
            while runner.runner_state['epoch'] < runner.configer.get('solver', 'max_epoch'):
                runner.train()
                if runner.runner_state['epoch'] == runner.configer.get('solver', 'max_epoch'):
                    runner.val()
                    break
        else:
            while runner.runner_state['iters'] < runner.configer.get('solver', 'max_iters'):
                runner.train()
                if runner.runner_state['iters'] == runner.configer.get('solver', 'max_iters'):
                    runner.val()
                    break

        Log.info('Training end...')

    @staticmethod
    def debug(runner):
        Log.info('Debugging start..')
        base_dir = os.path.join(runner.configer.get('project_dir'), 'out/vis',
                                runner.configer.get('task'), runner.configer.get('network', 'model_name'))

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        runner.debug(base_dir)
        Log.info('Debugging end...')

    @staticmethod
    def test(runner):
        Log.info('Testing start...')
        out_dir = os.path.join(runner.configer.get('project_dir'),
                               'results', runner.configer.get('task'),
                               runner.configer.get('dataset'),
                               runner.configer.get('network', 'checkpoints_name'),
                               runner.configer.get('test', 'out_dir'))

        test_img = runner.configer.get('test', 'img_path')
        test_dir = runner.configer.get('test', 'data_dir')
        if test_img is None and test_dir is None:
            Log.error('test_img & test_dir not exists.')
            exit(1)

        if test_img is not None:
            runner.test_img(test_img, out_dir)

        if test_dir is not None:
            runner.test(test_dir, out_dir)

        Log.info('Testing end...')
