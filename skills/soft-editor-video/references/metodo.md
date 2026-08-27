# Método de edição: referência

Detalhamento do pipeline da `SKILL.md`. Quando houver cena gerada, o caminho é **image-first**: gerar a imagem, aprovar e depois animar. A composição final é escolhida pela matéria-prima e pode usar tela cheia, apoio adaptativo, topo-fixo ou conteúdo puro.

## Por que cada passo
- **Corte de fala:** remover pausas e respirações; preservar o conteúdo. Corte semântico exige aprovação.
- **Fala temporizada:** preservar a transcrição por palavra com início e fim em `speech_words`, mesmo depois da compactação.
- **Mapa de cortes:** registrar cada trecho preservado com tempo na fonte, tempo na timeline e identificador único.
- **Emenda de áudio:** aplicar fade de 30 ms na entrada e na saída de cada trecho cortado.
- **Imagem:** usar a conta ChatGPT, sem chave OpenAI paga. Manter elementos importantes dentro da área segura.
- **Animação:** movimento local é o padrão de custo zero. Clipe externo usa imagem aprovada, prompt negativo, custo conferido e uma geração por vez.
- **Apoio adaptativo:** cada apoio dura de 2 a 3 segundos, salvo prova real que precise de tempo para leitura.
- **B-roll no rodapé:** quando essa forma for escolhida, usar faixa 16:9 embaixo com borda fina.
  - Se o vídeo do dono **já tem legenda** (geralmente embaixo), corta o teto morto acima da cabeça (`crop=1080:1312:0:~400`) e empilha (`vstack`). Assim cabe apresentador, legenda e b-roll sem cobrir nada.
- **CTA no final:** um card fixo (personagens + oferta do dono), colado com transição `xfade=fade:0.7` (sem corte seco).
- **Música de fundo:** SEMPRE discreta. Usar `loudnorm=I=-34` (achata o crescendo pra não ir subindo) + `volume=0.38`, mixada com `amix normalize=0` (mantém a fala cheia e a música baixa). Nunca sobrepõe a voz.

## Recursos

Ler `recursos-geracao.md`. Nunca usar chave OpenAI paga. Legenda usa o caminho local palavra por palavra. Vídeo externo é opcional, não pré-requisito.

## Ordem dos scripts
1. `00_silence_cut.py entrada.mp4 saida.mp4`
2. (agente escreve `scenes.json`) → `01_gen_images.py scenes.json pasta_img` → **aprovar com o dono**
3. `02_animate.py pasta_img pasta_video`
4. `03_assemble.py base.mp4 pasta_video montado.mp4 [overlay|crop]`, ou o template Remotion da forma escolhida
5. Aplicar todas as animações, faixas e overlays, e somente depois aplicar a legenda.
6. `04_build_final.py montado.mp4 candidato.mp4 [config/cta_take.mp4] [musica.mp3]`
7. `06_inspect_cuts.py candidato.mp4 edit-manifest.json pasta_cortes`
8. `07_gate_edit.py edit-manifest.json`
9. Exportar o final e rodar `06_audit.py final.mp4 pasta_audit 12 marcos_csv`

O candidato não recebe selo. Ele existe para conferir todas as emendas antes do gate. A auditoria final continua sendo feita somente no MP4 entregue.
