import { Kernel } from '@jupyterlab/services';
import { Token } from '@lumino/coreutils';
import { IJupyterYModel } from '../types';

export interface IJupyterYWidgetModelRegistry {
  getModel(id: string): IJupyterYModel | undefined;
}

export interface IJupyterYWidgetManager {
  registerKernel(kernel: Kernel.IKernelConnection): void;
  getWidgetModel(
    kernelId: string,
    commId: string
  ): IJupyterYModel | undefined;
}

export const IJupyterYWidgetManager = new Token<IJupyterYWidgetManager>(
  'jupyterYWidgetManager'
);
