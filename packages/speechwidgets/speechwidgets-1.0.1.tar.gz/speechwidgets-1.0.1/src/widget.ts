// Copyright (c) nicolvisser
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';
import ReactWidget from "./ReactWidget"
import React from 'react';
import ReactDOM from 'react-dom';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

// Your widget state goes here. Make sure to update the corresponding
// Python state in example.py
const defaultModelProperties = {
  src: 'blank',
  sxx: [[1.0, 0.0], [0.0, 1.0]],
  width: 900,
  spec_height: 300,
  nav_height: 50,
  navigator: true,
  settings: false,
  colormap: 'viridis',
  transparent: false,
  dark: false,
  annotations: [],
}

export type WidgetModelState = typeof defaultModelProperties

export class SpectrogramPlayerModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: SpectrogramPlayerModel.model_name,
      _model_module: SpectrogramPlayerModel.model_module,
      _model_module_version: SpectrogramPlayerModel.model_module_version,
      _view_name: SpectrogramPlayerModel.view_name,
      _view_module: SpectrogramPlayerModel.view_module,
      _view_module_version: SpectrogramPlayerModel.view_module_version,
      ...defaultModelProperties
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'SpectrogramPlayerModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'SpectrogramPlayerView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class SpectrogramPlayerView extends DOMWidgetView {
  render() {
    this.el.classList.add('custom-widget');

    const component = React.createElement(ReactWidget, {
      model: this.model,
    });
    ReactDOM.render(component, this.el);
  }
}
