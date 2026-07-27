document.addEventListener("DOMContentLoaded", () => {
  const progressLine = document.getElementById("progressLine");
  const circles = document.querySelectorAll(".circle");
  const cardsContainer = document.getElementById("cardsContainer");
  const timeline = document.querySelector(".timeline");

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

  const videosBtn = document.getElementById("videosBtn");
  const videosHome = document.getElementById("videosHome");
  const videoSlot = document.getElementById("videoSlot");

  const videosModal = document.getElementById("videosModal");
  const videosModalBackdrop = document.getElementById("videosModalBackdrop");
  const videosModalClose = document.getElementById("videosModalClose");
  const videosGrid = document.getElementById("videosGrid");
  const videosPlayer = document.getElementById("videosPlayer");
  const videosBack = document.getElementById("videosBack");
  const videoPlayerEl = document.getElementById("videoPlayerEl");
  const videoPlayerTitle = document.getElementById("videoPlayerTitle");
  const videosData = document.getElementById("videosData");

  const videoItems = videosData.querySelectorAll(".video-item");

  videoItems.forEach((item, index) => {
    const titulo = item.getAttribute("data-title") || `Vídeo ${index + 1}`;
    const src = item.getAttribute("data-src");

    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = "video-thumb";
    botao.innerHTML = `
      <span class="video-thumb-icon">▶</span>
      <span class="video-thumb-title">${titulo}</span>
    `;

    botao.addEventListener("click", () => {
      videoPlayerTitle.textContent = titulo;
      videoPlayerEl.src = src;
      videosGrid.hidden = true;
      videosPlayer.hidden = false;
      videoPlayerEl.play().catch(() => {});
    });

    videosGrid.appendChild(botao);
  });

  function abrirVideosModal() {
    videosModal.hidden = false;
  }

  function fecharVideosModal() {
    videosModal.hidden = true;
    videoPlayerEl.pause();
    videoPlayerEl.removeAttribute("src");
    videoPlayerEl.load();
    videosPlayer.hidden = true;
    videosGrid.hidden = false;
  }

  videosBtn.addEventListener("click", abrirVideosModal);
  videosModalClose.addEventListener("click", fecharVideosModal);
  videosModalBackdrop.addEventListener("click", fecharVideosModal);

  videosBack.addEventListener("click", () => {
    videoPlayerEl.pause();
    videosPlayer.hidden = true;
    videosGrid.hidden = false;
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !videosModal.hidden) {
      fecharVideosModal();
    }
  });

  function moverBotaoVideosPara(circle) {
    const circleRect = circle.getBoundingClientRect();
    const timelineRect = timeline.getBoundingClientRect();
    const centerX = circleRect.left + circleRect.width / 2 - timelineRect.left;

    videoSlot.style.left = `${centerX}px`;
    videoSlot.appendChild(videosBtn);
    videosHome.hidden = true;
  }

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

      moverBotaoVideosPara(circle);

      cardsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
});
