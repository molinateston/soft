# Adaptação do kit pro OpenRouter

O kit original chama a API direta da TypeSafe (`https://api.typesafe.ai/v1/systemone`, modelo `jev-1.13.0`, chave `TYPESAFE_API_KEY`). Aqui ele passa a chamar o Jev pelo OpenRouter com a menor mudança possível. O resto do kit (perguntas, filtro, cache, circuito, hooks, plugin, auto-melhoria) ficou igual.

## O que mudou

| Arquivo | Mudança |
|---|---|
| `codigo/src/contracts.mjs` | `ENDPOINT` padrão virou `https://openrouter.ai/api/alpha/decisions` e `MODEL` padrão virou `typesafe/jev-1.13`. Os dois aceitam troca por variável: `JEV_ENDPOINT` e `JEV_MODEL`. Nova função `modelMatches`: a resposta do OpenRouter traz o modelo com data (ex.: `typesafe/jev-1.13-20260917`), então a validação aceita o nome exato ou o nome seguido de `-sufixo`. Qualquer outro modelo continua recusado. |
| `codigo/src/client.mjs` | `resolveKey()` e `checkConfiguration()` leem primeiro `OPENROUTER_API_KEY`; `TYPESAFE_API_KEY` segue aceita como alternativa. |
| `codigo/hermes-plugin/jev-auto/credentials.py` | Considera `OPENROUTER_API_KEY` já presente no ambiente; quando a chave vem do gerenciador de senhas, repassa ao processo filho como `OPENROUTER_API_KEY`. |
| `codigo/hermes-plugin/tests/test_automation.py` | Dois testes passaram a esperar `OPENROUTER_API_KEY` no ambiente do filho. |

Os `.md` do kit (LEIA-ME, INSTALAR, COMO-FUNCIONA, AUTO-MELHORIA, PROMPT-ANALISE-90-DIAS, CHANGELOG) ficaram como vieram. Onde eles dizem `TYPESAFE_API_KEY`, leia `OPENROUTER_API_KEY`.

## Voltar pra API direta da TypeSafe

```sh
export JEV_ENDPOINT=https://api.typesafe.ai/v1/systemone
export JEV_MODEL=jev-1.13.0
export TYPESAFE_API_KEY=...   # e não defina OPENROUTER_API_KEY
```

## Conferido em 24/09/2026

- Chamada real pelo cliente do kit (choice, noul e score numa consulta): `available: true`, `choice: manual`, 358 ms, 392 tokens de entrada.
- `node src/cli.mjs --smoke`: `available: true`, 364 ms.
- `node src/cli.mjs --check`: mostra o endereço e o modelo do OpenRouter, `key_present: true`, sem imprimir a chave.
- Testes Python do plugin Hermes (`python3 -m unittest discover -s tests -p 'test_*.py'` dentro de `hermes-plugin/`): 38 de 38.

## Observação sobre a auto-melhoria

`codigo/auto-melhoria/medir.py` usa por padrão uma pontuação local, sem rede. Se um dia ligar a pontuação pelo Jev de verdade (o ponto de extensão `pontuacao_texto`), use o mesmo endereço, modelo e chave do OpenRouter acima.
