const { ipcRenderer } = require("electron");

const itemScreen = document.querySelectorAll(".item-screen");
const coffeeScreen = document.querySelector("#coffee");
const teeScreen = document.querySelector("#tee");
const smoothieScreen = document.querySelector("#smoothie");
const decaffeineScreen = document.querySelector("#decaffeine");
const beverageScreen = document.querySelector("#beverage");
const tabButtons = document.querySelectorAll(".tab-btn");

data = fetch("http://localhost:5000/menu")
  .then((response) => response.json())
  .then((data) => {
    data.forEach((element) => {
      const div = document.createElement("div");
      div.classList.add("item");
      const span = document.createElement("span");
      span.innerText = element.name;
      div.style.backgroundImage = `url('${element.img_path}')`;
      div.appendChild(span);
      div.addEventListener("click", () =>
        ipcRenderer.send("open-slide-window")
      );
      if (element.kind == "coffee") coffeeScreen.append(div);
      else if (element.kind == "tee") teeScreen.append(div);
      else if (element.kind == "smoothie") smoothieScreen.append(div);
      else if (element.kind == "decaffeine") decaffeineScreen.append(div);
      else if (element.kind == "beverage") beverageScreen.append(div);
      console.log(element.name);
    });
  })
  .catch((error) => console.error("Error:", error));

tabButtons.forEach((button) => {
  button.addEventListener("click", function () {
    const targetTab = button.dataset.tab;

    // 모든 버튼의 active 클래스 제거
    tabButtons.forEach((btn) => btn.classList.remove("active"));

    // 모든 패널의 active 클래스 제거
    itemScreen.forEach((panel) => panel.classList.remove("active"));

    // 클릭된 버튼과 해당 패널에 active 클래스 추가
    button.classList.add("active");
    document.getElementById(targetTab).classList.add("active");
  });
});
