# Régua adaptativa de edição

Use esta referência em talking-head, reels e anúncios que combinam apresentador com apoio visual.

## Escolha de composição

1. Prova real central: mostrar em tela inteira. Não reduzir Telegram, página, produto ou resultado real a uma faixa pequena.
2. Talking-head com explicação: usar composição adaptativa, com apresentador e apoio trocando de importância ao longo da fala.
3. Demonstração com muitas telas e slides: usar topo-fixo.
4. Conteúdo puro: preservar o quadro original e usar somente a HEADLINE temporária aprovada.

Nunca copiar automaticamente o formato do vídeo anterior.

## Régua aprovada dos anúncios

- Começar na primeira fala completa.
- Preservar toda a mensagem. Remover só pausa longa, respiração e erro evidente, salvo corte semântico aprovado.
- Usar 1,2x quando a família já estiver aprovada nessa velocidade.
- Manter o rosto centralizado e fechado, sem sobra acima da cabeça. Legenda na altura do peito.
- Trocar apoio a cada 2 a 3 segundos. Aceitar duração maior apenas para prova real que precise ser lida e registrar a exceção no manifesto.
- Priorizar imagem gerada e animada sobre cartela. Usar cartela somente quando nenhuma imagem ou tela representa melhor a fala.
- Acender a legenda palavra por palavra e destacar a palavra-chave do trecho.
- Revelar listas item por item, no instante em que cada item é falado.
- Fazer uma virada de layout por flash branco no terço inicial: apresentador grande em cima passa a close embaixo, enquanto o apoio ocupa cerca de dois terços superiores.
- Não fabricar print de notícia, tela de produto, painel, número ou resultado.
- Movimento local é o padrão. Cena gerada com créditos só entra por ordem do dono, após mostrar custo e receber o sim.

## Manifesto obrigatório

Criar `edit-manifest.json` com:

```json
{
  "final": "/caminho/final.mp4",
  "layout_mode": "adaptive",
  "caption_mode": "word",
  "keyword_highlight": true,
  "layout_flip_sec": 18.4,
  "layout_flip_ratio": 0.31,
  "speech_speed": 1.2,
  "speech_words": [
    {"word": "Implemente", "start": 0.0, "end": 0.42},
    {"word": "IA", "start": 0.44, "end": 0.63}
  ],
  "speech_compaction": {
    "source_duration": 8.4,
    "timeline_duration": 6.7,
    "removed_duration": 1.7,
    "word_timed": true
  },
  "cut_map": [
    {
      "id": "cut-001",
      "source_start": 0.0,
      "source_end": 3.2,
      "timeline_start": 0.0,
      "timeline_end": 3.2,
      "audio_fade_in_ms": 30,
      "audio_fade_out_ms": 30
    },
    {
      "id": "cut-002",
      "source_start": 4.9,
      "source_end": 8.4,
      "timeline_start": 3.2,
      "timeline_end": 6.7,
      "audio_fade_in_ms": 30,
      "audio_fade_out_ms": 30
    }
  ],
  "render_order": ["base", "animations_overlays", "captions", "music"],
  "cut_inspections": [
    {
      "cut_id": "cut-002",
      "passed": true,
      "proof": "/caminho/audit-cortes/cut-002/mosaico.jpg",
      "reviewer": "codex-oauth"
    }
  ],
  "semantic_cuts_approved": false,
  "support_segments": [
    {"start": 0.0, "end": 2.4, "type": "generated_image"},
    {"start": 2.4, "end": 5.1, "type": "real_screen"}
  ],
  "list_reveals": [
    {"label": "Comercial", "at": 12.2},
    {"label": "Marketing", "at": 13.1}
  ],
  "paid_generation": {"provider": "none", "credits": 0, "approved": true},
  "exceptions": []
}
```

Rodar `scripts/06_inspect_cuts.py` no candidato antes do gate. Depois rodar `scripts/07_gate_edit.py` antes do export final. A auditoria visual continua obrigatória depois do export.
