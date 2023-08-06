"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const application_1 = require("@jupyterlab/application");
const apputils_1 = require("@jupyterlab/apputils");
const widgets_1 = require("@lumino/widgets");
const launcher_1 = require("@jupyterlab/launcher");
const coreutils_1 = require("@jupyterlab/coreutils");
const lmod_js_1 = require("../../jupyterlmod/static/lmod.js");
const serverproxy = __importStar(require("@jupyterlab/server-proxy"));
function createModuleItem(label, button) {
    const lmod_list_line = document.createElement('li');
    const lmod_list_label = document.createElement('span');
    const lmod_list_button = document.createElement('button');
    lmod_list_line.append(lmod_list_label);
    lmod_list_line.append(lmod_list_button);
    lmod_list_line.setAttribute('class', 'jp-Lmod-item');
    lmod_list_label.setAttribute('class', 'jp-Lmod-itemLabel');
    lmod_list_label.innerText = label;
    lmod_list_button.setAttribute('class', 'jp-Lmod-itemButton jp-mod-styled');
    lmod_list_button.innerHTML = button;
    return lmod_list_line;
}
const lmodAPI = new lmod_js_1.Lmod(coreutils_1.PageConfig.getBaseUrl());
var global_launcher = null;
var kernelspecs = null;
var server_proxy_infos = {};
var server_proxy_launcher = {};
function updateLauncher(modulelist) {
    for (let server_key in server_proxy_infos) {
        let is_enabled = modulelist.some(module => { return module.toLowerCase().includes(server_key); });
        if (is_enabled) {
            if (!server_proxy_launcher.hasOwnProperty(server_key)) {
                server_proxy_launcher[server_key] = global_launcher.add(server_proxy_infos[server_key]);
            }
        }
        else if (server_proxy_launcher.hasOwnProperty(server_key)) {
            server_proxy_launcher[server_key].dispose();
            delete server_proxy_launcher[server_key];
        }
    }
}
async function show_module(module) {
    const data = await lmodAPI.show(module);
    const datalist = data.split('\n');
    const text = datalist.slice(3).join('\n').trim();
    const path = datalist[1].slice(0, -1);
    apputils_1.showDialog({
        title: module,
        body: new ModuleWidget(path, text),
        buttons: [
            apputils_1.Dialog.okButton()
        ]
    });
}
async function load_module(module) {
    const data = await lmodAPI.load([module]);
    if (data != null) {
        apputils_1.showDialog({
            title: "Module warning",
            body: new ModuleWidget("Warning", data),
            buttons: [apputils_1.Dialog.okButton()]
        });
    }
}
async function export_module() {
    const data = await lmodAPI.freeze();
    apputils_1.showDialog({
        title: "Export modules",
        body: new ModuleWidget("Add this in a notebook to load the same modules :", data),
        buttons: [
            apputils_1.Dialog.okButton()
        ]
    });
}
function save_collection(event) {
    return apputils_1.showDialog({
        title: 'Save collection',
        body: new SaveWidget(),
        buttons: [
            apputils_1.Dialog.cancelButton(),
            apputils_1.Dialog.okButton({ label: 'Save' })
        ]
    }).then(result => {
        if (result.button.label === 'Save') {
            let name = result.value;
            lmodAPI.save(name ? name : 'default');
        }
        return;
    });
}
/**
 * Main widget
 */
class LmodWidget extends widgets_1.Widget {
    constructor() {
        super();
        this.id = 'lmod-jupyterlab';
        this.title.caption = 'Softwares';
        this.title.iconClass = 'jp-LmodIcon jp-SideBar-tabIcon';
        this.addClass('jp-Lmod');
        const search_div = document.createElement('div');
        const search_div_wrapper = document.createElement('div');
        this.searchInput = document.createElement('input');
        search_div.setAttribute('class', 'jp-Lmod-search');
        search_div_wrapper.setAttribute('class', 'jp-Lmod-search-wrapper');
        this.searchInput.setAttribute('id', 'modules');
        this.searchInput.setAttribute('class', 'jp-Lmod-input');
        this.searchInput.setAttribute('placeholder', 'Filter available modules...');
        search_div.appendChild(search_div_wrapper);
        search_div_wrapper.appendChild(this.searchInput);
        this.node.insertAdjacentElement('afterbegin', search_div);
        this.node.insertAdjacentHTML('beforeend', `<div id="lmod" class="jp-Lmod-content">
          <div class="jp-Lmod-section">
              <div class="jp-Lmod-sectionHeader"><H2>Loaded Modules</H2>
                  <button
                    title="Create collection"
                    class="jp-Lmod-collectionButton jp-mod-styled jp-AddIcon"
                    id="save-button"
                  ></button>
                  <button
                    title="Restore collection"
                    class="jp-Lmod-collectionButton jp-mod-styled jp-UndoIcon"
                    id="restore-button"
                  ></button>
                  <button
                    title="Generate Python code"
                    class="jp-Lmod-collectionButton jp-mod-styled jp-CopyIcon"
                    id="export-button"
                  ></button>
              </div>
              <div class="jp-Lmod-sectionContainer">
                  <ul class="jp-Lmod-sectionList" id="lmod_loaded_list">
                  </ul>
              </div>
          </div>
          <div class="jp-Lmod-section">
              <div class="jp-Lmod-sectionHeader">
                <h2 id="lmod_avail_header">Available Modules</h2>
              </div>
              <div class="jp-Lmod-sectionContainer">
                <ul class="jp-Lmod-sectionList" id="lmod_avail_list">
                </ul>
              </div>
          </div>
      </div>`);
        this.loadedUList = this.node.querySelector('#lmod_loaded_list');
        this.availUList = this.node.querySelector('#lmod_avail_list');
        this.availHeader = this.node.querySelector('#lmod_avail_header');
        this.loadedUList.addEventListener('click', this.onClickModuleList.bind(this));
        this.availUList.addEventListener('click', this.onClickModuleList.bind(this));
        const buttons = this.node.getElementsByClassName('jp-Lmod-collectionButton');
        buttons['save-button'].addEventListener('click', save_collection);
        buttons['restore-button'].addEventListener('click', this.restore.bind(this));
        buttons['export-button'].addEventListener('click', export_module);
        this.searchInput.addEventListener('keyup', this.updateAvail.bind(this));
    }
    async onClickModuleList(event) {
        const target = event.target;
        if (target.tagName == 'SPAN') {
            show_module(target.innerText);
        }
        else if (target.tagName == 'BUTTON') {
            const span = event.target.closest('li').querySelector('span');
            const item = span.innerText;
            if (target.innerText == 'Load') {
                await load_module(item);
            }
            else if (target.innerText == 'Unload') {
                await lmodAPI.unload([item]);
            }
            this.update();
        }
    }
    update() {
        Promise.all([lmodAPI.avail(), lmodAPI.list()])
            .then(values => {
            const avail_set = new Set(values[0]);
            const modulelist = values[1];
            const html_list = modulelist.map(item => createModuleItem(item, 'Unload'));
            this.loadedUList.innerText = '';
            this.loadedUList.append(...html_list);
            modulelist.map(item => avail_set.delete(item));
            this.searchSource = Array.from(avail_set);
            this.updateAvail();
            updateLauncher(modulelist);
        });
        kernelspecs.refreshSpecs();
    }
    updateAvail() {
        const input = this.searchInput.value;
        this.availUList.innerText = '';
        const result = this.searchSource.filter(str => str.toUpperCase().includes(input.toUpperCase()));
        const html_list = result.map(item => createModuleItem(item, 'Load'));
        this.availUList.append(...html_list);
        this.availHeader.innerText = `Available Modules (${result.length})`;
    }
    restore(event) {
        return apputils_1.showDialog({
            title: 'Restore collection',
            body: new RestoreWidget(),
            buttons: [
                apputils_1.Dialog.cancelButton(),
                apputils_1.Dialog.okButton({ label: 'Restore' })
            ]
        }).then(result => {
            if (result.button.label === 'Restore') {
                const name = result.value;
                lmodAPI.restore(name).then(() => this.update());
            }
            return;
        });
    }
}
/**
 * Class that intercepts items that would be
 * added to JupyterLab launcher by jupyter-server-proxy
 * to either add them to the launcher if their name
 * is in the launcher pin list, or keep them in a
 * seperate data structure until the corresponding
 * module is loaded.
 */
class ILauncherProxy {
    constructor(launcher_pins) {
        this.launcher_pins = launcher_pins;
    }
    add(item) {
        let name = item.args.id.split(':')[1];
        if (this.launcher_pins.includes(name.toLowerCase())) {
            global_launcher.add(item);
        }
        else {
            server_proxy_infos[name] = item;
        }
    }
}
async function setup_proxy_commands(app, restorer) {
    let launcher_pins = [];
    const pin_response = await fetch(coreutils_1.PageConfig.getBaseUrl() + 'lmod/launcher-pins');
    if (pin_response.ok) {
        const data = await pin_response.json();
        launcher_pins = data.launcher_pins.map(pin => pin.toLowerCase());
    }
    else {
        console.log('jupyter-lmod: could not communicate with jupyter-lmod API.');
    }
    let tmp_launcher = new ILauncherProxy(launcher_pins);
    serverproxy.default.activate(app, tmp_launcher, restorer);
}
/**
 * Activate the lmod widget extension.
 */
function activate(app, palette, restorer, launcher) {
    const widget = new LmodWidget();
    global_launcher = launcher;
    kernelspecs = app.serviceManager.kernelspecs;
    setup_proxy_commands(app, restorer);
    restorer.add(widget, 'lmod-sessions');
    app.shell.add(widget, 'left', { rank: 1000 });
    widget.update();
    console.log('JupyterFrontEnd extension lmod is activated!');
}
;
const extension = {
    id: 'jupyterlab_lmod',
    autoStart: true,
    requires: [apputils_1.ICommandPalette, application_1.ILayoutRestorer, launcher_1.ILauncher],
    activate: activate
};
class SaveWidget extends widgets_1.Widget {
    constructor() {
        let body = document.createElement('div');
        let text = document.createElement('label');
        text.innerHTML = "Enter a new collection name:";
        body.appendChild(text);
        let input = document.createElement('input');
        input.placeholder = "default";
        body.appendChild(input);
        super({ node: body });
    }
    getValue() {
        return this.node.querySelector('input').value;
    }
}
class RestoreWidget extends widgets_1.Widget {
    constructor() {
        let body = document.createElement('div');
        let text = document.createElement('label');
        text.innerHTML = "Select a collection to restore :";
        body.appendChild(text);
        let selector = document.createElement('select');
        lmodAPI.savelist()
            .then(values => {
            values.map((item, index) => {
                let opt = document.createElement("option");
                opt.value = item;
                opt.text = item;
                selector.add(opt);
            });
        });
        body.appendChild(selector);
        super({ node: body });
    }
    getValue() {
        return this.node.querySelector('select').value;
    }
}
class ModuleWidget extends widgets_1.Widget {
    constructor(labelText, content) {
        let body = document.createElement('div');
        let label = document.createElement('label');
        label.innerHTML = labelText;
        body.appendChild(label);
        let div = document.createElement('div');
        div.classList.add('jp-JSONEditor-host');
        div.setAttribute("style", "min-height:inherit;");
        let text = document.createElement('pre');
        text.setAttribute("style", "margin:10px 10px; white-space:pre-wrap;");
        text.innerHTML = content;
        div.appendChild(text);
        body.appendChild(div);
        super({ node: body });
    }
}
exports.default = extension;
