const { app, BrowserWindow, webContents } = require("electron");

WIDTH = 600;
HEIGHT = 800;

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: WIDTH,
    height: HEIGHT,
    webPreferences: {
      contextIsolation: false,
      nodeIntegration: true,
    },
    // frame: false,
  });

  mainWindow.loadFile("./index.html");

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.on("ready", createWindow);
app.on("activate", () => {
  if (mainWindow === null) createWindow();
});
