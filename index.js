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

  // --- Ajuste de altura do card (corrige o corte de texto no mobile) ---
  //
  // Antes, a abertura do card usava um max-height fixo em CSS (1000px),
  // suficiente no desktop, mas não no celular: com a tela mais estreita,
  // o mesmo texto ocupa mais altura (por causa das imagens flutuantes
  // .foto-lateral reduzindo o espaço horizontal disponível), ultrapassa
  // os 1000px e o excesso fica cortado pelo overflow:hidden.
  //
  // Agora a altura é calculada a partir do conteúdo real
  // (cardsContentInner.scrollHeight). Depois que a transição termina,
  // trocamos o max-height para "none", removendo qualquer limite —
  // assim o conteúdo nunca mais é cortado, independente do tamanho da
  // tela, do texto ou de quando as imagens terminam de carregar.

  function alturaAtualDoConteudo() {
    return cardsContentInner.scrollHeight;
  }

  cardsContent.addEventListener("transitionend", (evento) => {
    if (
      evento.propertyName === "max-height" &&
      cardsContent.classList.contains("aberto")
    ) {
      cardsContent.style.maxHeight = "none";
    }
  });

  function abrirCard() {
    cardsContent.classList.add("aberto");
    arrow.classList.remove("rotacionado");
    requestAnimationFrame(() => {
      cardsContent.style.maxHeight = alturaAtualDoConteudo() + "px";
    });
  }

  function fecharCard() {
    // Se estiver "none" (após já ter terminado de abrir), primeiro
    // volta para um valor em pixels para permitir a transição suave
    // até 0, já que o navegador não anima a partir de "none".
    if (
      cardsContent.style.maxHeight === "none" ||
      cardsContent.style.maxHeight === ""
    ) {
      cardsContent.style.maxHeight = alturaAtualDoConteudo() + "px";
      // força o navegador a aplicar o valor acima antes de mudar de novo
      void cardsContent.offsetHeight;
    }
    requestAnimationFrame(() => {
      cardsContent.classList.remove("aberto");
      arrow.classList.add("rotacionado");
      cardsContent.style.maxHeight = "0px";
    });
  }

  // Reajusta a altura se alguma imagem do conteúdo ainda estiver
  // carregando quando o card for aberto (evita corte por imagem que
  // "cresce" depois que a altura já tinha sido calculada).
  function observarImagensDoConteudo() {
    const imagens = cardsContentInner.querySelectorAll("img");
    imagens.forEach((img) => {
      if (!img.complete) {
        img.addEventListener("load", () => {
          if (cardsContent.classList.contains("aberto")) {
            cardsContent.style.maxHeight = "none";
          }
        });
      }
    });
  }

  cardsHeader.addEventListener("click", () => {
    const estaAberto = cardsContent.classList.contains("aberto");
    if (estaAberto) {
      fecharCard();
    } else {
      abrirCard();
    }
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
      abrirCard();
      observarImagensDoConteudo();

      moverBotaoVideosPara(circle);

      cardsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
});
