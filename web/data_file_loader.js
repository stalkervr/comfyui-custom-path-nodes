//import { api } from "../../../scripts/api.js";
//import { app } from "../../../scripts/app.js";
//
//const NODE_NAME = "DataFileSelector";
//
//async function fetchNamesForSource(source) {
//  const body = new FormData();
//  body.append("source", source);
//
//  try {
//    const response = await fetch("/datafile/names_for_source", {
//      method: "POST",
//      body: body,
//    });
//
//    const data = await response.json();
//    console.log(`[${NODE_NAME}] Received names for source '${source}':`, data.names);
//    return data.names;
//  } catch (error) {
//    console.error(`[${NODE_NAME}] Error fetching names:`, error);
//    return [];
//  }
//}
//
//app.registerExtension({
//  name: `custom.${NODE_NAME}`,
//
//  async beforeRegisterNodeDef(nodeType, nodeData, app) {
//    if (nodeData.name !== NODE_NAME) return;
//
//    const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
//
//    nodeType.prototype.onNodeCreated = function () {
//      const node = this;
//      const result = originalOnNodeCreated?.apply(this);
//
//      const sourceWidget = node.widgets.find((w) => w.name === "source");
//      const nameWidget = node.widgets.find((w) => w.name === "name");
//
//      if (!sourceWidget || !nameWidget) {
//        console.warn(`[${NODE_NAME}] Widgets not found`);
//        return result;
//      }
//
//      // Обновление списка имён при выборе source
//      sourceWidget.callback = async () => {
//        const selectedSource = sourceWidget.value;
//        nameWidget.value = "loading...";
//        node.setDirtyCanvas(true, true);
//
//        const names = await fetchNamesForSource(selectedSource);
//        nameWidget.options.values = names;
//        nameWidget.value = names[0] || "";
//        node.setDirtyCanvas(true, true);
//      };
//
//      return result;
//    };
//  },
//});

import { api } from "../../../scripts/api.js";
import { app } from "../../../scripts/app.js";

const NODE_NAME = "DataFileLoader";

async function fetchNamesForSource(source) {
  const body = new FormData();
  body.append("source", source);

  try {
    const response = await fetch("/datafile/names_for_source", {
      method: "POST",
      body: body,
    });

    const data = await response.json();
    console.log(`[${NODE_NAME}] Received names for source '${source}':`, data.names);
    return data.names;
  } catch (error) {
    console.error(`[${NODE_NAME}] Error fetching names:`, error);
    return [];
  }
}

app.registerExtension({
  name: `custom.${NODE_NAME}`,

  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name !== NODE_NAME) return;

    const originalOnNodeCreated = nodeType.prototype.onNodeCreated;

    nodeType.prototype.onNodeCreated = function () {
      const node = this;
      const result = originalOnNodeCreated?.apply(this);

      const sourceWidget = node.widgets.find((w) => w.name === "source");
      const nameWidget = node.widgets.find((w) => w.name === "name");

      if (!sourceWidget || !nameWidget) {
        console.warn(`[${NODE_NAME}] Widgets not found`);
        return result;
      }

      // Обновление списка имён при выборе source
      sourceWidget.callback = async () => {
        const selectedSource = sourceWidget.value;
        nameWidget.value = "loading...";
        node.setDirtyCanvas(true, true);

        const names = await fetchNamesForSource(selectedSource);
        nameWidget.options.values = names;
        nameWidget.value = names[0] || "";
        node.setDirtyCanvas(true, true);
      };

      return result;
    };
  },
});

