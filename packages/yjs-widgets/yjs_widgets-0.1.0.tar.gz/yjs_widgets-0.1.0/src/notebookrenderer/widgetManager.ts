import { Kernel, KernelMessage } from '@jupyterlab/services';
import { JupyterYModel } from '../model';
import {
  IJupyterYWidgetModelRegistry,
  IJupyterYWidgetManager
} from './token';
import { YCommProvider } from './yCommProvider';
import { IJupyterYModel } from '../types';

export class JupyterYWidgetManager implements IJupyterYWidgetManager {
  registerKernel(kernel: Kernel.IKernelConnection): void {
    const wm = new WidgetModelRegistry({ kernel });
    this._registry.set(kernel.id, wm);
  }

  unregisterKernel(kernelId?: string | null): void {
    if (kernelId) {
      this._registry.delete(kernelId);
    }
  }

  getWidgetModel(
    kernelId: string,
    commId: string
  ): IJupyterYModel | undefined {
    return this._registry.get(kernelId)?.getModel(commId);
  }

  private _registry = new Map<string, IJupyterYWidgetModelRegistry>();
}

export class WidgetModelRegistry implements IJupyterYWidgetModelRegistry {
  constructor(options: {
    kernel: Kernel.IKernelConnection;
  }) {
    const { kernel } = options;
    kernel.registerCommTarget('@jupyterlab:ywidget', this._handle_comm_open);
  }

  getModel(id: string): IJupyterYModel | undefined {
    return this._yModels.get(id);
  }

  /**
   * Handle when a comm is opened.
   */
  private _handle_comm_open = async (
    comm: Kernel.IComm,
    msg: KernelMessage.ICommOpenMsg
  ): Promise<void> => {
    const yModel = new JupyterYModel({});

    new YCommProvider({
      comm,
      ydoc: yModel.sharedModel.ydoc
    });
    this._yModels.set(comm.commId, yModel);
  };

  private _yModels: Map<string, IJupyterYModel> = new Map();
}
