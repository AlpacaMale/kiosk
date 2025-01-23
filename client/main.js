const { app, BrowserWindow, webContents } = require("electron");

WIDTH = 600;
HEIGHT = 800;

let mainWindow;
let slideWindow;

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
  mainWindow.webContents.openDevTools();
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

function createSlideWindow() {
  slideWindow = new BrowserWindow({
    width: WIDTH,
    height: HEIGHT,
    frame: false,
    // transparent: true,
  });

  slideWindow.loadURL("./option.html");
}

app.on("ready", createWindow);
app.on("activate", () => {
  if (mainWindow === null) createWindow();
});
