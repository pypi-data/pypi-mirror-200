import { Panel } from '@lumino/widgets';

import { NotebookRendererModel } from './model';
import { IRenderMime } from '@jupyterlab/rendermime';
import { IJupyterYModel } from '../types';

export const CLASS_NAME = 'mimerenderer-jupytercad';

export class NotebookRenderer extends Panel implements IRenderMime.IRenderer {
  /**
   * Construct a new output widget.
   */
  constructor(options: { factory: NotebookRendererModel; mimeType: string }) {
    super();
    this._modelFactory = options.factory;
    this._mimeType = options.mimeType;
    this.addClass(CLASS_NAME);
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }
    this._jcadModel?.dispose();
    super.dispose();
  }
  async renderModel(mimeModel: IRenderMime.IMimeModel): Promise<void> {
    const { commId } = JSON.parse(mimeModel.data[this._mimeType] as string) as {
      commId: string;
    };

    this._jcadModel = await this._modelFactory.createYModel(commId);
    if (!this._jcadModel) {
      return;
    }
  }

  private _modelFactory: NotebookRendererModel;
  private _mimeType: string;
  private _jcadModel?: IJupyterYModel;
}
