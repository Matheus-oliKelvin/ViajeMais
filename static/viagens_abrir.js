function toggleCard() {
      /* Declara a função chamada quando o cabeçalho é clicado.
         Ela alterna o estado (fechado/aberto) do conteúdo. */

      const conteudo = document.getElementById("viagem-conteudo");
      /* Busca no DOM o elemento com id 'card-content' e guarda na constante 'content'. */

      conteudo.classList.toggle("open");
      /* Alterna a classe 'open' nesse elemento:
         - Se a classe NÃO existir, adiciona (abrindo: aplica .card-content.open).
         - Se a classe JÁ existir, remove (fechando: volta para .card-content).
         A mudança da classe dispara a transição de 'max-height' definida no CSS.
          content.classList.toggle("open") é como um interruptor de luz para a classe "open".

        Se está apagada (classe ausente), ele acende (adiciona a classe).

        Se está acesa (classe presente), ele apaga (remove a classe).*/
}