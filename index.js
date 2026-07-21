document.addEventListener("DOMContentLoaded", () => {
  const progressLine = document.getElementById("progressLine");
  const circles = document.querySelectorAll(".circle");
  const cardsContainer = document.getElementById("cardsContainer");

  const card = document.getElementById("card");
  const cardsHeader = document.getElementById("cardsHeader");
  const cardsTitle = document.getElementById("cardsTitle");
  const cardsContent = document.getElementById("cardsContent");
  const cardsContentInner = document.getElementById("cardsContentInner");
  const arrow = card.querySelector(".arrow-icon");

  const conteudosData = document.getElementById("conteudosData");

  function getConteudo(position) {
    const bloco = conteudosData.querySelector(`[data-position="${position}"]`);
    return bloco ? bloco.innerHTML : "<p>Conteúdo em desenvolvimento...</p>";
  }

  cardsHeader.addEventListener("click", () => {
    cardsContent.classList.toggle("aberto");
    arrow.classList.toggle("rotacionado");
  });

  circles.forEach((circle) => {
    circle.addEventListener("click", () => {
      const position = circle.getAttribute("data-position");

      progressLine.style.width = `${position}%`;

      circles.forEach((c) => c.classList.remove("active"));
      circle.classList.add("active");

      cardsTitle.textContent = circle.querySelector(".date").textContent;
      cardsContentInner.innerHTML = getConteudo(position);

      card.hidden = false;
      cardsContent.classList.add("aberto");
      arrow.classList.remove("rotacionado");

      cardsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
});
