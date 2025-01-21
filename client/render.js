// const { ipcRenderer } = require("electron");
const itemScreen = document.querySelector(".item-screen");

data = fetch("http://localhost:5000/menu")
  .then((response) => response.json())
  .then((data) => {
    data.forEach((element) => {
      const div = document.createElement("div");
      div.classList.add("item");
      const span = document.createElement("span");
      span.innerText = element.name;
      div.style.backgroundImage = `url('${element.img_path}')`;
      console.log(element.img_path);
      div.appendChild(span);
      itemScreen.append(div);
      console.log(element.name);
    });
  })
  .catch((error) => console.error("Error:", error));
