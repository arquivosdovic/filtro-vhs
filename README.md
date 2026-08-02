# VHS-IZER 3000

Duas ferramentas standalone (um único arquivo `.html` cada, sem instalação) que aplicam um filtro de fita VHS envelhecida — scan lines, aberração cromática, ruído, distorção de tracking, desfoque, saturação/temperatura de cor, preto e branco e vinheta — em **fotos** ou **vídeos**, com corte 4:3 opcional. Tudo roda localmente no navegador: nada é enviado a servidor nenhum.

## Arquivos

| Arquivo | Para quê serve |
|---|---|
| `vhs-filter.html` | Aplica o filtro em **imagens** (JPEG, PNG, HEIC/HEIC, etc.). Exporta PNG ou GIF animado. |
| `vhs-video.html` | Aplica o filtro em **vídeos**. Exporta MP4. |

Cada arquivo é autocontido — basta abrir no navegador (duas exceções abaixo, sobre `vhs-video.html`).

## Como usar

1. Abra o arquivo desejado no navegador (Chrome, Firefox ou Edge recomendados).
2. Clique em **Carregar foto** / **Carregar vídeo** e selecione o arquivo.
3. Ajuste os controles de fita à direita — a prévia atualiza em tempo real, mesmo pausado.
4. (Opcional) Clique em **Cropar em 4:3** para recortar o enquadramento — veja detalhes abaixo.
5. Baixe o resultado.

### Controles de fita

Todos vão de 0 a 100 e têm 4 atalhos prontos (**Leve**, **Clássico**, **Fita podre**, **P&B**):

- **Scan lines** — linhas horizontais escurecidas, características de tubo CRT.
- **Aberração cromática** — desalinhamento horizontal dos canais R/G/B.
- **Ruído / grão** — grão aleatório sobre a imagem.
- **Distorção de tracking** — faixas horizontais deslocadas, como uma fita mal trackeada.
- **Desfoque** — suaviza a imagem.
- **Saturação/cor quente** — reduz saturação e empurra o tom para âmbar/magenta.
- **Preto e branco** — mistura com escala de cinza.
- **Vinheta** — escurece as bordas.

### Corte 4:3

Disponível nas duas versões, com o mesmo fluxo:

1. Clique em **Cropar em 4:3** — abre uma caixa de seleção arrastável sobre a imagem/vídeo original, com um slider de **Tamanho do corte**.
2. Posicione e redimensione a caixa.
3. Clique em **Aplicar corte**, ou **Cancelar** para desistir.
4. Para ajustar depois, clique em **Ajustar corte 4:3**; para descartar, **Remover corte**.

Na versão de **foto**, o corte é aplicado na hora (o preview já mostra o resultado final cortado). Na de **vídeo**, a caixa é só uma referência visual — o corte de fato acontece durante a exportação do MP4.

### Exportação

- **`vhs-filter.html`**: baixa uma imagem PNG estática, ou um **GIF animado** (14 quadros com leve jitter de tracking, redimensionado para até 480px).
- **`vhs-video.html`**: extrai os quadros do vídeo, aplica o efeito em cada um e remonta um **MP4** (áudio preservado, se houver). Também é possível ajustar **FPS de saída** (8–24) e **resolução** (480–854px de largura), além de cortar um **trecho** do vídeo com um slider de trim.

## Requisitos e observações técnicas

- **Conexão com a internet é necessária na primeira execução** — ambos os arquivos carregam bibliotecas de CDN:
  - `vhs-filter.html`: `heic2any` (conversão de HEIC) e `gif.js` (exportação de GIF).
  - `vhs-video.html`: `ffmpeg.wasm` (extração/remontagem de vídeo).
- **`vhs-video.html` precisa ser servido por um servidor local**, em vez de aberto por duplo clique (`file://`) — o `ffmpeg.wasm` depende de `SharedArrayBuffer`, que só fica disponível se a página for servida com os cabeçalhos `Cross-Origin-Opener-Policy` e `Cross-Origin-Embedder-Policy`. Um `python3 -m http.server` comum **não** envia esses cabeçalhos e resulta no erro `SharedArrayBuffer is not defined`. Por isso, use o `servidor.py` incluído, que já adiciona os headers certos: na pasta do arquivo, rode
  ```
  python3 servidor.py
  ```
  e abra `http://localhost:8000/vhs-video.html`.
- Vídeos longos ou em alta resolução podem levar alguns minutos para processar — o processamento é feito quadro a quadro, no próprio navegador.
- Para desempenho, a foto é trabalhada em até 900px no maior lado, e a prévia ao vivo do vídeo em até 480px de largura; a exportação final do vídeo usa a resolução escolhida no seletor.

## Estrutura de cada arquivo

Cada `.html` é autocontido: CSS, HTML e JavaScript num único arquivo, sem build step. A lógica de efeito (`applyVhsEffects`/`render`) é a mesma base em ambas as versões, adaptada para operar sobre uma imagem estática ou sobre cada quadro extraído do vídeo.
