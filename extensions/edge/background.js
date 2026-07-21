let port = null;

function connectNative() {
    try {
        port = chrome.runtime.connectNative("com.observex.host");

        port.onMessage.addListener((msg) => {
            console.log("ObserveX Agent:", msg);
        });

        port.onDisconnect.addListener(() => {
            console.log("Native host disconnected.");

            if (chrome.runtime.lastError) {
                console.error(chrome.runtime.lastError.message);
            }

            port = null;
        });

    } catch (e) {
        console.error(e);
    }
}

connectNative();

function sendToAgent(tab) {

    if (!port)
        connectNative();

    if (!port)
        return;

    port.postMessage({
        event: "tab_changed",
        url: tab.url || "",
        title: tab.title || "",
        tabId: tab.id,
        windowId: tab.windowId,
        timestamp: Date.now()
    });
}

chrome.tabs.onActivated.addListener(async (activeInfo) => {
    const tab = await chrome.tabs.get(activeInfo.tabId);
    sendToAgent(tab);
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete") {
        sendToAgent(tab);
    }
});