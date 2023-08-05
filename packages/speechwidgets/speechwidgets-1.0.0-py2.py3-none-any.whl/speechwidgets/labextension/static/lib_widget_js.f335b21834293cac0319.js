(self["webpackChunkspeechwidgets"] = self["webpackChunkspeechwidgets"] || []).push([["lib_widget_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./lib/ReactWidget.js":
/*!****************************!*\
  !*** ./lib/ReactWidget.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const widget_model_1 = __webpack_require__(/*! ./hooks/widget-model */ "./lib/hooks/widget-model.js");
const react_audio_spectrogram_player_1 = __importDefault(__webpack_require__(/*! react-audio-spectrogram-player */ "webpack/sharing/consume/default/react-audio-spectrogram-player/react-audio-spectrogram-player"));
function ReactWidget(props) {
    const [src] = widget_model_1.useModelState('src');
    const [sxx] = widget_model_1.useModelState('sxx');
    const [width] = widget_model_1.useModelState('width');
    const [specHeight] = widget_model_1.useModelState('spec_height');
    const [navHeight] = widget_model_1.useModelState('nav_height');
    const [navigator] = widget_model_1.useModelState('navigator');
    const [settings] = widget_model_1.useModelState('settings');
    const [colormap] = widget_model_1.useModelState('colormap');
    const [transparent] = widget_model_1.useModelState('transparent');
    const [dark] = widget_model_1.useModelState('dark');
    const [annotations] = widget_model_1.useModelState('annotations');
    return (react_1.default.createElement("div", { className: "Widget", style: { width: width } },
        react_1.default.createElement(react_audio_spectrogram_player_1.default, { src: src, sxx: sxx, specHeight: specHeight, navHeight: navHeight, navigator: navigator, settings: settings, colormap: colormap, transparent: transparent, dark: dark, annotations: annotations })));
}
function withModelContext(Component) {
    return (props) => (react_1.default.createElement(widget_model_1.WidgetModelContext.Provider, { value: props.model },
        react_1.default.createElement(Component, Object.assign({}, props))));
}
exports["default"] = withModelContext(ReactWidget);


/***/ }),

/***/ "./lib/hooks/widget-model.js":
/*!***********************************!*\
  !*** ./lib/hooks/widget-model.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.useModel = exports.useModelEvent = exports.useModelState = exports.WidgetModelContext = void 0;
const react_1 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
exports.WidgetModelContext = react_1.createContext(undefined);
// HOOKS
//============================================================================================
/**
 *
 * @param name property name in the Python model object.
 * @returns model state and set state function.
 */
function useModelState(name) {
    const model = useModel();
    const [state, setState] = react_1.useState(model === null || model === void 0 ? void 0 : model.get(name));
    useModelEvent(`change:${name}`, (model) => {
        setState(model.get(name));
    }, [name]);
    function updateModel(val, options) {
        model === null || model === void 0 ? void 0 : model.set(name, val, options);
        model === null || model === void 0 ? void 0 : model.save_changes();
    }
    return [state, updateModel];
}
exports.useModelState = useModelState;
/**
 * Subscribes a listener to the model event loop.
 * @param event String identifier of the event that will trigger the callback.
 * @param callback Action to perform when event happens.
 * @param deps Dependencies that should be kept up to date within the callback.
 */
function useModelEvent(event, callback, deps) {
    const model = useModel();
    const dependencies = deps === undefined ? [model] : [...deps, model];
    react_1.useEffect(() => {
        const callbackWrapper = (e) => model && callback(model, e);
        model === null || model === void 0 ? void 0 : model.on(event, callbackWrapper);
        return () => void (model === null || model === void 0 ? void 0 : model.unbind(event, callbackWrapper));
    }, dependencies);
}
exports.useModelEvent = useModelEvent;
/**
 * An escape hatch in case you want full access to the model.
 * @returns Python model
 */
function useModel() {
    return react_1.useContext(exports.WidgetModelContext);
}
exports.useModel = useModel;


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) nicolvisser
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) nicolvisser
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.SpectrogramPlayerView = exports.SpectrogramPlayerModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const ReactWidget_1 = __importDefault(__webpack_require__(/*! ./ReactWidget */ "./lib/ReactWidget.js"));
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_dom_1 = __importDefault(__webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom"));
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
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
};
class SpectrogramPlayerModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign(Object.assign({}, super.defaults()), { _model_name: SpectrogramPlayerModel.model_name, _model_module: SpectrogramPlayerModel.model_module, _model_module_version: SpectrogramPlayerModel.model_module_version, _view_name: SpectrogramPlayerModel.view_name, _view_module: SpectrogramPlayerModel.view_module, _view_module_version: SpectrogramPlayerModel.view_module_version }), defaultModelProperties);
    }
}
exports.SpectrogramPlayerModel = SpectrogramPlayerModel;
SpectrogramPlayerModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
SpectrogramPlayerModel.model_name = 'SpectrogramPlayerModel';
SpectrogramPlayerModel.model_module = version_1.MODULE_NAME;
SpectrogramPlayerModel.model_module_version = version_1.MODULE_VERSION;
SpectrogramPlayerModel.view_name = 'SpectrogramPlayerView'; // Set to null if no view
SpectrogramPlayerModel.view_module = version_1.MODULE_NAME; // Set to null if no view
SpectrogramPlayerModel.view_module_version = version_1.MODULE_VERSION;
class SpectrogramPlayerView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add('custom-widget');
        const component = react_1.default.createElement(ReactWidget_1.default, {
            model: this.model,
        });
        react_dom_1.default.render(component, this.el);
    }
}
exports.SpectrogramPlayerView = SpectrogramPlayerView;


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"speechwidgets","version":"1.0.0","description":"A library with Jupyter widgets for speech processing","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css","preview.png"],"homepage":"https://github.com//speechwidgets","bugs":{"url":"https://github.com//speechwidgets/issues"},"license":"BSD-3-Clause","author":{"name":"nicolvisser","email":"nicolvisser@yahoo.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com//speechwidgets"},"scripts":{"build":"npm run build:lib && npm run build:nbextension && npm run build:labextension:dev","build:prod":"npm run build:lib && npm run build:nbextension && npm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"npm run clean:lib && npm run clean:nbextension && npm run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf speechwidgets/labextension","clean:nbextension":"rimraf speechwidgets/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"npm run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","react":"^17.0.2","react-audio-spectrogram-player":"^1.0.1","react-dom":"^17.0.2"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@babel/preset-react":"^7.14.5","@babel/preset-typescript":"^7.14.5","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/react":"^17.0.11","@types/react-dom":"^17.0.8","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","babel-loader":"^8.2.2","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"babel":{"presets":["@babel/preset-env","@babel/preset-react","@babel/preset-typescript"]},"jupyterlab":{"extension":"lib/plugin","outputDir":"speechwidgets/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.f335b21834293cac0319.js.map