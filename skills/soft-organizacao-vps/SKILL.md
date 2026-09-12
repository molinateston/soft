---
name: soft-organizacao-vps
description: >-
  Faz faxina num servidor Linux e libera espaço em disco sem perder nada: mede o que ocupa, classifica cada item em 4 baldes (nuvem, quarentena, apaga, fica), sobe pra nuvem o que é pesado antes de qualquer remoção, move pra quarentena com manifesto reversível, e só apaga com autorização nominal. Entrega relatório antes e depois com os GB liberados e o comando de reverter. Use quando o pedido for: "faxina na VPS", "limpa o servidor", "o disco está cheio", "libera espaço", "no space left on device", "o que está pesando aí", "sobe esses vídeos pra nuvem", "arquiva o que não uso", "organiza o servidor", "revisa a quarentena", "simula a limpeza antes". NÃO use pra: construir ou editar sistema, site ou automação (soft-sistema); publicar documento no Drive (soft-google-docs); organizar a rotina do time (soft-gestao-agil); arquivos do computador pessoal; backup completo ou migração; performance de aplicação. Leia e siga o fluxo inteiro do SKILL.md.
---

# Faxina de servidor

Esta skill libera espaço num servidor Linux sem perder nada que o dono ainda queira. Mede o disco, classifica cada item em quatro baldes, sobe pra nuvem o que é pesado, move o duvidoso pra quarentena reversível, e só apaga com autorização nominal. No fim entrega um relatório com os GB liberados e o comando exato de desfazer cada movimento.

**O que é "pronto" nesta skill (vale pra toda ação).** A entrega só existe quando a pasta de saída tem os arquivos da ação MAIS `conferencia/checagem-titulos.md` (saída de `scripts/checar_titulos.py`, preenchida) e `python3 scripts/checar_titulos.py --conferir <pasta de saída> --insumos <pasta de insumos do dono> --perfil <perfil do dono>` devolve exit 0. A última linha dessa saída vai colada no relato ou no handoff. Na pasta de saída o dono vê só o entregável e o handoff; todo arquivo de conferência (checagem-titulos.md, titulos.txt, teses.txt, nomes.txt, conferir.txt) mora em `conferencia/`. O relato abre com três linhas: `Pronto:` · `Abra primeiro:` · `Falta você responder:` e fecha com `Perguntas pra você`. Headline nunca em caixa alta. Sem isso, não diga "pronto": diga o que falta. **O caminho de `--insumos` é a RAIZ que contém o perfil do dono, nunca uma subpasta dela**, e o comando colado no relato é literalmente o comando desta linha: o script imprime `insumos resolvido: <caminho>` e reprova a forma quando o perfil mora fora da pasta de insumos. O passo a passo da régua está em `references/regua-de-titulos.md`. Esta skill é a pasta instalada que contém este arquivo e a subpasta `scripts/` (confira com `ls scripts/checar_titulos.py` a partir dela); se você leu este arquivo de um plugin, cache ou cópia sem `scripts/`, pare e abra a pasta instalada.

**`ls -l` e `diff=0` são linhas de saída do gate, nunca prosa.** No bloco de entrega, junto do `--conferir`, colam-se as duas: o `ls -l` do arquivo na raiz e o `diff` devolvendo 0. O `--conferir` procura as duas na pasta quando existir arquivo casando `faxina-*.md` e imprime `prova do relatório: ls -l colado: sim/não · diff=0 colado: sim/não`, saindo com exit 1 quando faltar qualquer uma.

**A linha do inventário aparece duas vezes na entrega, e só duas:** uma na peça que o dono lê e uma no `conferencia/checagem-titulos.md`. Recitar a linha dentro do RELATO não conta como prova, porque o RELATO já cola a saída do gate, que a contém. Cole `linhas de inventário na entrega: 2`.

**Exit diferente de 0 não é entrega, mesmo com o relato honesto.** As linhas que o script imprime dizem o que corrigir, e corrigir uma linha de contagem custa menos que entregar uma peça reprovada. Depois de corrigir, rode de novo e cole a saída nova.

**Comando mental:** *medir, propor, autorizar, subir, mover, só então apagar.* **Regra de ouro:** nada sai do disco sem cópia verificada na nuvem ou sem o dono ter dito o nome do item. Quarentena é o padrão, remoção é exceção.

**Três números que valem antes de qualquer passo:** quarentena vence em **30 dias** (padrão sugerido, o dono pode mudar e o número dele entra no relatório) · meta de uso do disco **abaixo de 70%** da partição · autorização genérica vale só pros baldes NUVEM e QUARENTENA, nunca pro balde APAGA.

**Antes de começar, veja o exemplo.** `references/EXEMPLO-FIM-A-FIM.md` mostra uma faxina inteira num caso fictício: a medição crua, a tabela de classificação, a proposta que o dono aprovou por número, o manifesto preenchido linha a linha, a simulação, o relatório final e uma reversão de verdade. Ler antes evita a rodada de retrabalho mais comum, que é propor sem número.

## A condução: a skill te ajuda a fazer, não só te entrega

Esta skill é um agente que conduz, e o padrão está em `references/09-conducao-agente.md`. Como aqui a skill mexe em arquivo de servidor, o "modo" é sobre o nível de autorização, e valem sempre a parte 1 (pergunta o modo) e a parte 4 (oferece refinar).

**Pergunta o modo, uma vez, logo na primeira mensagem, nesta linha:**

> Antes de começar: te mostro item a item e você aprova cada balde antes de eu mexer, ou você já autoriza mover tudo que eu marcar (e eu te mostro o plano completo antes de executar)? De um jeito ou de outro, nada é apagado sem o seu OK, e o que sai vai pra quarentena com manifesto antes de qualquer remoção. Se não responder, sigo no modo item a item.

- **Modo item a item** (default, e o que roda no silêncio): mostra cada balde da classificação e espera o dono aprovar antes de mover, um de cada vez.
- **Modo autorizo tudo que você marcar**: mostra o plano completo dos 4 baldes de uma vez, o dono aprova o conjunto, e a skill move o que marcou pra quarentena. Mesmo aqui, apagar de vez continua sendo passo separado, só depois do prazo da quarentena e com OK explícito.

**Oferece refinar no fim (parte 4):** depois do relatório antes e depois, fecha com UMA linha: "Quer que eu tire algum item do plano, mude o prazo da quarentena, ou já feche o ciclo apagando o que venceu? Me diz que eu ajusto." A oferta de refino não substitui o gate nem o passo estreito de remoção.


## Roteamento por pedido

| O dono pediu | Ação |
|---|---|
| "faxina na VPS", "disco cheio", "libera espaço", "o que está pesando", "no space left on device" | **Faxina completa: passos 0 a 7, na ordem** |
| "me mostra o que dá pra limpar sem mexer em nada", "simula", "quanto eu ganharia" | **Passos 0 a 3 em modo simulação**, sem executar nada (ver "Modo simulação") |
| "sobe esses vídeos pra nuvem", "arquiva a mídia antiga" | **Passos 0, 1 e 2 restritos ao balde NUVEM**, depois passo 4 |
| "revisa a quarentena", "o que está vencido no arquivo", "pode apagar o que já passou do prazo" | **Revisão de quarentena** (bloco próprio, no fim) |
| "reverte aquilo que você moveu" | **Reversão pelo manifesto** (passo 5, bloco "Reverter um movimento") |

Pedido ambíguo ("dá uma organizada aí"): pergunte uma coisa só, se o objetivo é liberar espaço agora ou entender primeiro o que ocupa, e siga pela resposta. Na dúvida, comece pela simulação, ela não muda nada e responde as duas.

## Como ler cada passo

Cada passo abaixo traz o mesmo bloco fixo: **O que faz** · **Precisa de** (o insumo e de onde vem) · **Sem o insumo** (o caminho concreto quando falta) · **Entrega** (o que sai, com nome de arquivo quando for arquivo).

---

## 0. Antes de tudo: pergunte a raiz e a nuvem

**O que faz:** fecha o contrato da faxina, a pasta onde você pode mexer e o destino da nuvem.

**Precisa de:** a raiz da faxina e o conector de nuvem disponível, os dois perguntados ao dono.

**Sem o insumo:** raiz não respondida, use a pasta de trabalho atual e diga em uma linha que assumiu isso. Nuvem não respondida, você descobre sozinho no passo 4.

**Regra da variável sem resposta.** Variável sem resposta entra como `[A CONFIRMAR: o quê]` SEM valor assumido; é proibido inventar número, data ou nome e etiquetar.

**Entrega:** as duas respostas registradas no topo do relatório, elas são o contrato da faxina.

Pergunte as duas numa mensagem só:

1. **Qual a raiz da faxina?** A pasta a partir da qual você pode olhar e mexer (a home do usuário, ou a pasta de projetos). Chame de `RAIZ` daqui pra frente. Nunca assuma uma raiz, nunca use caminho de outra máquina.
2. **Tem nuvem conectada?** Qual conector existe no ambiente (armazenamento em objeto, drive, bucket, servidor remoto por sincronização).

---

## 1. Medir (só leitura, nada muda)

**O que faz:** levanta os números do disco antes de qualquer opinião.

**Precisa de:** a raiz do passo 0 e acesso de leitura ao servidor.

**Sem o insumo:** comando ausente no ambiente, use o que existir e registre a lacuna no relatório. Nunca invente número.

**Entrega:** uma tabela com item, tamanho e data do último acesso. Sem opinião ainda.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

Nenhuma proposta antes dos números. Rode o que o ambiente permitir e guarde a saída:

```bash
RAIZ="${RAIZ:-$PWD}"

df -h                                        # uso por partição, a foto geral
du -h -d 2 "$RAIZ" 2>/dev/null | sort -rh | head -40   # as pastas mais pesadas
find "$RAIZ" -type f -size +100M -printf '%s\t%p\n' 2>/dev/null | sort -rn | head -40   # os maiores arquivos
```

A tabela de alvos clássicos, com o comando de medir cada um separado (mídia pesada, logs, caches, dependências reinstaláveis, builds antigos, duplicatas, órfãos), está em `references/medicao-e-falhas.md`. O número decide, nunca o palpite.

### Checagem de serviço vivo (rode para CADA pasta candidata, antes de classificar)

Pasta que um serviço em execução usa não entra na faxina. Este é o comando pronto, cole a pasta no lugar de `<PASTA>`:

```bash
ALVO="<PASTA>"

# 1. algum processo tem arquivo aberto dentro da pasta?
lsof +D "$ALVO" 2>/dev/null | awk 'NR>1{print $1, $2}' | sort -u

# 2. algum serviço aponta pra pasta na própria definição?
grep -rl "$ALVO" /etc/systemd/system /lib/systemd/system 2>/dev/null

# 3. algum processo em execução tem a pasta na linha de comando ou no diretório de trabalho?
ps -eo pid,comm,args | grep -F "$ALVO" | grep -v grep
ls -l /proc/*/cwd 2>/dev/null | grep -F "$ALVO"

# 4. algum ponto de montagem ou volume de contêiner vive ali?
# ATENÇÃO: `findmnt -T` NUNCA vem vazio pra pasta comum, porque ele devolve a
# partição MÃE (quase sempre a mesma da raiz). Ler a saída crua como "montagem
# própria" classifica TUDO como vivo e zera a faxina. Compare com a raiz: só é
# montagem própria quando o alvo tem um ponto de montagem DIFERENTE do da raiz.
RAIZ="<RAIZ DA FAXINA>"
MNT_ALVO=$(findmnt -T "$ALVO" -no TARGET 2>/dev/null)
MNT_RAIZ=$(findmnt -T "$RAIZ" -no TARGET 2>/dev/null)
[ -n "$MNT_ALVO" ] && [ "$MNT_ALVO" != "$MNT_RAIZ" ] && echo "montagem própria: $MNT_ALVO"
```

**Leitura do resultado:** qualquer uma das quatro devolvendo linha, a pasta é **VIVA**. Marque no relatório como `FICA (serviço ativo: <nome>)` e não proponha movimento. Se o dono quiser mexer mesmo assim, ele para o serviço primeiro, e isso é decisão dele, não sua. Todas as quatro vazias, a pasta é candidata e segue pro passo 2.

**A checagem 4 só conta quando o alvo tem montagem PRÓPRIA.** Cole no relatório os dois valores, `MNT_ALVO` e `MNT_RAIZ`, lado a lado. Iguais, a checagem 4 é **vazia** e não marca nada como vivo. Rodada em que TODOS os itens saíram como FICA por causa da checagem 4 é sinal de que ela foi lida crua: refaça a comparação antes de entregar uma faxina que não move nada.

Ambiente sem `lsof`, use as outras três e registre no relatório que a checagem foi parcial.

---

## 2. Classificar em 4 baldes

**O que faz:** coloca cada item medido em exatamente um balde, com o motivo em uma linha.

**Precisa de:** a tabela do passo 1 e o resultado da checagem de serviço vivo.

**Sem o insumo:** item cuja origem ninguém sabe explicar vai pra QUARENTENA, nunca pra APAGA.

**Entrega:** a tabela dos 4 baldes, com item, tamanho, balde e motivo.

Cada item medido entra em exatamente um balde. Escreva o motivo em uma linha.

| Balde | O que entra | Destino |
|---|---|---|
| **NUVEM** | Vídeo, render, imagem grande, áudio, zip de entrega, texto antigo que o dono ainda quer consultar. Pesado e raramente lido. | Sobe, verifica, depois sai do disco |
| **QUARENTENA** | Provável lixo, mas com dúvida: projeto parado, saída de build antiga, pasta que ninguém sabe de onde veio. | Move pra `_ARQUIVO/`, apaga só depois do prazo |
| **APAGA** | Reproduzível ou descartável de verdade: cache, log rotacionado, dependência reinstalável, temporário, duplicata idêntica confirmada. | Remoção direta, ainda assim com autorização |
| **FICA** | Código vivo, configuração, dado de aplicação em uso, credencial, banco, repositório versionado. | Não toca |

Regras de classificação que não se negociam:

- Em dúvida entre dois baldes, escolha o mais conservador (FICA vence QUARENTENA, QUARENTENA vence APAGA).
- Nada vai pro balde APAGA só por ser grande. Grande e insubstituível vai pra NUVEM.
- Dependência reinstalável só entra em APAGA se existir o arquivo de manifesto que a reconstrói no mesmo projeto.

---

## 3. Mostrar o plano e pedir autorização item a item

**O que faz:** transforma a classificação numa lista numerada que o dono autoriza item por item.

**Precisa de:** a tabela do passo 2 e o uso atual do disco do passo 1.

**Sem o insumo:** faltando o tamanho de algum item, ele entra na lista com `[A CONFIRMAR]` no lugar do número e não conta no total previsto.

**Entrega:** a proposta no formato abaixo, e um **STOP**. Sem a lista de números do dono, nada acontece.

Antes de qualquer `mv` ou remoção, mostre a proposta assim, um balde por bloco e um número por item:

```
Uso atual: 87% (172G de 197G) · meta sugerida: abaixo de 70%

NUVEM (sobe, verifica, e só então sai do disco)  ..........  41 GB
  1. gravacoes/2025/           28 GB   último acesso há 8 meses
  2. renders/entregas-antigas/ 13 GB   último acesso há 5 meses

QUARENTENA (move, apaga só depois de 30 dias)  ............  12 GB
  3. projeto-parado-x/          9 GB   sem alteração há 1 ano
  4. build-antigo/              3 GB   substituído pela versão nova

APAGA (reproduzível)  ....................................  22 GB
  5. cache do gerenciador de pacote  14 GB   reinstala sozinho
  6. logs rotacionados > 90 dias      8 GB   já comprimidos

FICA (não toco)
  código, configuração, banco, repositórios versionados, pasta com serviço ativo

Total previsto liberado: 75 GB  ·  uso final estimado: 49%

Responda os NÚMEROS que autoriza (exemplo: "1, 2, 5"). O que não for citado, não acontece.
```

Pare aqui. Sem a lista de números do dono, você não executa nada. Autorização genérica ("pode limpar tudo") vale só pros baldes NUVEM e QUARENTENA, nunca pro balde APAGA: pra apagar, o dono cita o item.

### Modo simulação (nada muda no disco)

Pedido de "simula", "me mostra o que aconteceria" ou "quanto eu ganharia": rode os passos 0 a 3 e **pare na proposta**, sem executar nada. A saída é a mesma lista numerada, com o cabeçalho `SIMULAÇÃO, nada foi executado`, mais o que cada número faria:

```
SIMULAÇÃO, nada foi executado. Nenhum arquivo saiu do lugar.

Item 1 · gravacoes/2025/   28 GB
  faria: subir pra nuvem, verificar por soma de verificação, depois mover pra
         $RAIZ/_ARQUIVO/2026-08-07-faxina/midia/gravacoes-2025/
  reverteria com: mv "$RAIZ/_ARQUIVO/2026-08-07-faxina/midia/gravacoes-2025" "$RAIZ/gravacoes/2025"
  serviço vivo: nenhum (lsof, systemd, ps e findmnt vazios)

Total que sairia do disco: 75 GB · uso final estimado: 49% (hoje 87%)
Itens que a simulação NÃO tocaria: 3 pastas com serviço ativo (listadas acima como FICA)
```

Toda linha sai da medição real do passo 1. Simulação com número inventado é pior que não simular; tamanho não medido aparece como `[A CONFIRMAR]` e fica fora do total. Depois, ofereça em uma linha: "posso executar os itens que você citar por número". Não execute nada por iniciativa própria.

---

## 4. Subir pra nuvem antes de apagar

**O que faz:** copia pra nuvem, verifica a cópia, e só então o original vira candidato a sair do disco.

**Precisa de:** os itens do balde NUVEM autorizados por número no passo 3, e um conector de nuvem no ambiente.

**Sem o insumo:** sem conector nenhum, não improvise e não apague. Gere `SUBIR-PRA-NUVEM.md` na raiz com a lista de caminhos, tamanhos e o comando pronto pro dono rodar depois de conectar a conta dele. Esses itens saem da faxina de hoje e viram pendência declarada no relatório.

**Entrega:** cada item verificado, com o método de verificação registrado, e o original movido pra quarentena com a nota de onde a cópia ficou.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

Só pros itens autorizados do balde NUVEM. Descubra o que o ambiente tem e use o primeiro que existir:

```bash
command -v rclone gdrive aws gcloud az rsync scp 2>/dev/null
```

- **Se houver conector de sincronização genérico:** use o modo que copia e depois confere, com verificação de integridade ligada.
- **Se houver cliente de armazenamento em objeto:** copie recursivo pro bucket que o dono indicar, depois liste o destino e compare.
- **Se houver só acesso a outra máquina:** sincronize por cópia remota com checagem.
- **Se não houver conector nenhum:** não improvise e não apague. Gere um arquivo `SUBIR-PRA-NUVEM.md` na raiz com a lista de caminhos, os tamanhos e o comando pronto pra o dono rodar depois de conectar a conta dele. Esses itens saem da faxina de hoje e viram pendência declarada no relatório.

**Verificação obrigatória antes de o arquivo sair do disco.** Um dos dois, nesta ordem de preferência:

```bash
# preferido: soma de verificação, compare a lista da origem com a do destino
find <origem> -type f -exec sha256sum {} \; | awk '{print $1}' | sort > /tmp/origem.sha
# gere a mesma lista no destino e compare
diff /tmp/origem.sha /tmp/destino.sha && echo "IGUAL, pode remover a origem"

# aceitável quando o destino não expõe soma: contagem de arquivos e bytes batendo
find <origem> -type f | wc -l ; du -sb <origem>
```

Se a verificação falhar ou não for possível, o item volta pro balde QUARENTENA. Nunca some com o original.

Depois de verificado, o original **não é apagado direto**: vai pra quarentena com a nota "já está na nuvem em `<destino>`". Assim ainda dá pra reverter no prazo.

---

## 5. Quarentena com manifesto

**O que faz:** move o item pra uma pasta datada e registra cada movimento numa linha que permite desfazer.

**Precisa de:** os itens autorizados dos baldes QUARENTENA e NUVEM (estes depois de verificados).

**Sem o insumo:** item que não está no manifesto fica onde está, sempre. Manifesto é a condição do movimento, não o registro dele.

**Entrega:** `$RAIZ/_ARQUIVO/AAAA-MM-DD-faxina/` com `MANIFEST.txt` e `README.md` preenchidos.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.

Estrutura, sempre relativa à `RAIZ` que o dono indicou:

```
$RAIZ/_ARQUIVO/AAAA-MM-DD-motivo/
   MANIFEST.txt         origem -> destino, tamanho, motivo, quem autorizou
   README.md            o que é essa rodada, prazo, como reverter
   <subpastas por tipo> midia/  builds/  projetos-parados/  logs/
```

Como mover e registrar, um item por vez:

```bash
Q="$RAIZ/_ARQUIVO/$(date +%F)-faxina"
mkdir -p "$Q/midia"
echo "$(date +%F)|<origem>|$Q/midia/<nome>|<tamanho>|<motivo>|autorizado por: dono, item N" >> "$Q/MANIFEST.txt"
mv "<origem>" "$Q/midia/"
```

**Um `MANIFEST.txt` preenchido de verdade tem esta cara** (exemplo fictício, seis campos separados por barra vertical):

```
# MANIFEST da rodada 2026-08-07-faxina · raiz: /srv/projetos · prazo: vence em 2026-09-06
# data|origem|destino|tamanho|motivo|autorizacao
2026-08-07|/srv/projetos/gravacoes/2025|/srv/projetos/_ARQUIVO/2026-08-07-faxina/midia/gravacoes-2025|28G|balde NUVEM, ja copiado e verificado por sha256 em bucket-arquivo/gravacoes-2025|dono autorizou item 1
2026-08-07|/srv/projetos/app/build-antigo|/srv/projetos/_ARQUIVO/2026-08-07-faxina/builds/build-antigo|3,2G|balde QUARENTENA, substituido pela versao 4.1|dono autorizou item 4
```

E o `README.md` da mesma rodada abre com raiz, contagem de itens, total movido, a data em que o prazo vence, quem autorizou, e o comando de reverter um item por extenso. O molde completo está em `references/EXEMPLO-FIM-A-FIM.md`.

Regras da quarentena:

- Uma rodada por data. Se já existe pasta da mesma data, complete o `MANIFEST.txt` dela em vez de abrir outra.
- **Rodada fechada não é raiz fechada.** Se `_ARQUIVO/AAAA-MM-DD-faxina/` já existe **e já tem `MANIFEST.txt` preenchido**, a rodada daquela data está encerrada: **não repita a classificação dos itens já movidos** e não reivindique o trabalho dela como seu. Checagem verificável antes de começar: liste os itens que já constam no `MANIFEST.txt` e os itens que você vai classificar agora, e prove que as duas listas não se cruzam; item repetido nas duas reprova a rodada.
- **O delta da rodada nova tem DUAS fontes, nunca uma.** (a) O que mudou no disco, medido por `find` e `du` contra os números da rodada anterior. (b) **O que a rodada anterior deixou PENDENTE**, que é a fonte que mais se perde: item classificado como FICA por falta de uma confirmação, item proposto e não autorizado, pergunta aberta no relatório. Antes de concluir qualquer coisa, rode `grep -n 'A CONFIRMAR\|pendente\|proposta\|aguardando' <relatório da rodada anterior> <MANIFEST.txt da rodada anterior>` e trate CADA linha devolvida como candidata desta rodada. Uma autorização que chegou depois resolve um item que ficou parado, sem que um único byte tenha mudado no disco: nesse caso o disco está igual e o delta não é zero. Ler "nada mudou no disco" como "nada a fazer" é o erro que esta regra existe pra matar. As duas fontes saem LISTADAS no relatório, uma seção cada, mesmo quando uma delas vier vazia. Checagem colada: `delta de disco: N itens · pendências da rodada anterior: N · resolvidas ou reafirmadas nesta rodada: N · sem destino: 0`.
- **E o relatório sai SEMPRE, inclusive com delta zero nas duas fontes.** Grave `faxina-AAAA-MM-DD.md` na raiz do dono com as linhas medi, delta e o que vence quando, ainda que ele tenha três linhas. O relatório de delta zero é curto e é justamente o que prova que a rodada aconteceu: sem ele, o próximo agente que abrir a raiz vê o relatório da data anterior e conclui que ninguém passou por ali hoje. **Entrega sem esse arquivo na raiz reprova a rodada**, porque o relato de processo da sessão é registro do agente e o `faxina-AAAA-MM-DD.md` é o documento do dono, e um nunca substitui o outro. Não inventar movimento pra parecer produtivo continua valendo, e é outra coisa: não inventar movimento é sobre o disco, entregar o relatório é sobre o documento.
- Todo `mv` vira uma linha no manifesto **antes** de acontecer. Sem linha, sem movimento.
- Se algum processo ainda aponta pro caminho antigo, deixe um `README.md` de aviso no lugar de origem dizendo pra onde foi.
- Nunca devolva pro lugar original uma pasta que outra rodada acabou de mover.

**Reverter um movimento:**

```bash
# leia a linha no MANIFEST.txt e desfaça exatamente ela
mv "$Q/midia/<nome>" "<origem-listada-no-manifesto>"
```

Sem inventar destino. Item que não está no manifesto fica onde está.

---

## 6. Apagar, o passo mais estreito

**O que faz:** remove, um item por vez, só o que passou pelas duas condições abaixo.

**Precisa de:** autorização nominal do dono para aquele item, ou o prazo de quarentena vencido e confirmado por ele.

**Sem o insumo:** sem uma das duas, não remove. Fica na quarentena e vira linha de pendência no relatório.

**Entrega:** cada remoção registrada no relatório com a autorização citada.

Só pode ser removido o que satisfizer uma das duas condições:

1. Está na quarentena há **N dias ou mais** (padrão sugerido: 30 dias) e o dono confirmou a passagem do prazo; ou
2. O dono autorizou **nominalmente** aquele item na lista do passo 3.

Antes de remover, mostre o que vai sair e confirme uma última vez:

```bash
# sempre liste antes de remover
du -sh <alvo> ; ls -la <alvo>
```

Nunca use remoção recursiva com curinga solto, nunca remova dentro de uma varredura automática. Um alvo por vez, nomeado.

---

## 7. Relatório antes e depois

**O que faz:** fecha a faxina num arquivo que o dono consegue ler daqui a três meses e entender o que aconteceu.

**Precisa de:** os números do passo 1 (antes), a medição repetida ao fim (depois), e o manifesto da rodada.

**Sem o insumo:** item que não pôde ser medido no fim entra como `[A CONFIRMAR]`, nunca como estimativa.

**Entrega:** `faxina-AAAA-MM-DD.md` na raiz combinada.

**O relatório da faxina se prova com `ls -l` e com `diff`.** Cole, na lista de saída:

```
ls -l --time-style=full-iso <raiz>/faxina-AAAA-MM-DD.md
diff <raiz>/faxina-AAAA-MM-DD.md <saída>/faxina-AAAA-MM-DD.md; echo diff=$?
```

A primeira linha vai inteira, como o shell devolveu. A segunda tem que devolver `diff=0`. Dono ou tamanho diferentes do seu arquivo significam que a raiz tem o relatório de outra sessão: grave o seu e rode de novo.

**Afirmação de verificação só vale com a saída crua colada.** Frase que afirma um resultado de comando (`confirmei`, `checado`, `medi`, `confere`, `verificado`, `conferido`) sai com o bloco cercado logo abaixo, com a saída literal do shell. **Sem a saída, a frase sai da entrega.** Numa skill de infraestrutura isto reprova a rodada, porque é a única linha que o dono não confere sem abrir o terminal. O `checar_titulos.py` conta e reprova, em `afirmações de verificação sem saída colada: N (teto 0)`.

**Arquivos obrigatórios: os arquivos acima, e `conferencia/checagem-titulos.md` por último (saída de `scripts/checar_titulos.py`, ver `references/regua-de-titulos.md`).** Confira com `ls conferencia/checagem-titulos.md` antes de dizer que entregou. Esta skill pode entregar zero título: o `conferencia/checagem-titulos.md` sai assim mesmo, com `títulos no lote: 0` e as linhas de lint, marcadores e piso do perfil, que o script cobre em qualquer entrega.
**Os dois destinos não competem, o relatório vai nos dois.** O `faxina-AAAA-MM-DD.md` e o `MANIFEST.txt` são documentos DA RAIZ do dono e vivem lá, sempre: é onde o próximo agente e o próprio dono vão procurar na rodada seguinte. Uma cópia no diretório de saída da sessão satisfaz o pedido da rodada e não substitui a da raiz. Quando o pedido mandar os entregáveis pra uma pasta específica, grave nos dois lugares e declare `relatório na raiz do dono: <caminho absoluto> · cópia na saída: <caminho absoluto>`, provando com a saída de `ls -l <raiz>/faxina-AAAA-MM-DD.md` colada. **Entrega sem o arquivo na raiz reprova a rodada**, mesmo com o mesmo arquivo presente na saída, e escolher um destino em detrimento do outro nunca é a leitura certa: nada no pedido proíbe gravar na raiz, e a raiz é o objeto desta skill.

Entregue um arquivo `.md` na raiz combinada, nomeado `faxina-AAAA-MM-DD.md`, com:

- **Números primeiro:** uso do disco antes e depois, GB liberados, percentual final contra a meta.
- **O que subiu pra nuvem:** caminho de origem, destino, tamanho, como foi verificado.
- **O que foi pra quarentena:** pasta da rodada, quantidade de itens, GB, data em que o prazo vence.
- **O que foi apagado:** item por item, com a autorização citada.
- **O que não foi tocado e por quê:** inclusive o que ficou pendente por falta de conector de nuvem.
- **Como reverter:** o comando de revert de um item, apontando pro manifesto.
- **As duas fontes do delta, em seções próprias:** o que mudou no disco desde a rodada anterior, e as pendências que a rodada anterior deixou abertas, cada pendência com o veredito desta rodada (resolvida, reafirmada como pendente, ou descartada com motivo). Seção vazia sai escrita como vazia, nunca omitida.
- **Data de último acesso sai com a origem da medição ao lado.** Escreva `último acesso: <data> (fonte: atime)` ou `(fonte: mtime, aproximado)`; onde o sistema não guarda atime confiável, é PROIBIDO registrar a data de hoje como último acesso, porque a data de hoje é a da sua própria varredura e não a do uso. Item sem medição confiável entra como `último acesso: [A CONFIRMAR: atime indisponível]` e nunca embasa sozinho uma proposta de apagar.

Bullet vence parágrafo. Número vence adjetivo. Sem changelog do seu próprio trabalho.

---

## Revisão de quarentena (a rodada que fecha o ciclo)

**O que faz:** varre as quarentenas antigas, separa as que venceram, e devolve ao dono uma lista de decisão.

**Precisa de:** a raiz, e as pastas `_ARQUIVO/` que existirem dentro dela.

**Sem o insumo:** nenhuma pasta `_ARQUIVO/` encontrada, diga isso em uma linha e pare. Não vasculhe o resto do disco atrás de coisa pra apagar.

**Entrega:** uma lista numerada de itens vencidos, com o mesmo formato de autorização do passo 3.

Sem esta rodada, a quarentena vira um depósito e o disco enche de novo pela porta dos fundos. Rode quando o dono pedir, e ofereça sempre que passar por uma raiz que já tem `_ARQUIVO/`.

```bash
RAIZ="${RAIZ:-$PWD}"; HOJE=$(date +%s)
for d in "$RAIZ"/_ARQUIVO/*/; do
  [ -d "$d" ] || continue
  nome=$(basename "$d"); data=$(echo "$nome" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}')
  [ -n "$data" ] || { echo "$nome | sem data no nome, revise à mão"; continue; }
  dias=$(( (HOJE - $(date -d "$data" +%s)) / 86400 ))
  tam=$(du -sh "$d" 2>/dev/null | cut -f1)
  itens=$(grep -vc '^#' "$d/MANIFEST.txt" 2>/dev/null || echo "sem manifesto")
  echo "$nome | $tam | $itens itens | $dias dias | $( [ "$dias" -ge 30 ] && echo VENCIDA || echo "vence em $((30-dias))d" )"
done
```

Com a lista na mão, as cinco decisões:

1. **Rodada VENCIDA:** abra o `MANIFEST.txt` dela e monte a lista numerada no formato do passo 3. Espere os números do dono. Vencimento não é autorização.
2. **Rodada sem manifesto:** ninguém sabe de onde veio, então ela não é candidata a remoção. Vira pendência: "rodada X sem manifesto, precisa de decisão sua item a item".
3. **Item já verificado na nuvem:** diga isso na linha da proposta, porque muda a decisão do dono.
4. **Autorizado:** remova pelo passo 6, um item por vez, e grave `revisao-quarentena-AAAA-MM-DD.md` no formato do passo 7.
5. **O dono quer segurar mais tempo:** anote o novo prazo no `README.md` da rodada e siga. Prazo é dele, não seu.

Linha removida vira `# REMOVIDO em AAAA-MM-DD, autorizado por: dono` no manifesto, nunca apagada: o histórico é o que prova o que aconteceu. Rodada esvaziada por inteiro, remova a pasta vazia e registre. Uma revisão completa está em `references/EXEMPLO-FIM-A-FIM.md`.

---

## Gate de qualidade (antes de dizer que a faxina terminou)

**Uso completo do que o dono deu (vale em toda entrega desta skill).** Todo dado que o dono forneceu e cabe na entrega tem que aparecer nela ou ter o motivo da exclusão declarado. Checagem verificável antes de fechar: liste os dados que o dono deu, um por linha, na forma `<dado> | usado em <onde> ou descartado porque <motivo>`, e feche com `Dados fornecidos: N · usados: N · descartados com motivo: N · sem destino: 0.` Qualquer dado em `sem destino` reprova a entrega. A linha de fechamento vai no arquivo de entrega que o dono lê, nunca só no relato de processo. **A granularidade é a do dado que o dono forneceu: agrupar vários dados numa linha só reprova o crivo.** Um dado por linha, mesmo quando dois parecem do mesmo assunto, porque agrupado ninguém confere qual dos dois ficou de fora. **O piso é CONTADO, não estimado:** conte os dados do perfil do dono um a um (com shell, `grep -c '^-' <perfil>` dá o número de campos) e desdobre os campos de valor múltiplo, porque oferta com preço, parcela, 3 bônus e garantia são 6 linhas, não 1. Cole a conta na entrega, nesta forma: `dados no perfil: N · usados: N · descartados com motivo: N`, e a soma de usados mais descartados tem que fechar em N. **Entrega sem essa contagem reprova sem análise de conteúdo**, e inventário com menos linhas que N também reprova. **A unidade do inventário é o bullet de primeiro nível do perfil**, contado por `grep -c '^- ' <perfil>` com a saída do comando colada ao lado do número. Bullet que carrega vários valores entra como UMA linha com os valores enumerados dentro dela, e o total nunca ultrapassa o número que o comando devolveu. Declarar um total maior que a saída do comando reprova a linha de fechamento, porque conta valor onde a régua conta campo; declarar menor reprova a entrega sem análise de conteúdo. Sem shell, conte os bullets à mão e escreva `contagem manual` ao lado do número.

**O piso do inventário é contável e a conta vai colada.** Rode `grep -c '^- ' <perfil>` e cole a saída do comando: esse número é o PISO BRUTO. Depois desdobre toda linha que carrega mais de um valor (a oferta com preço, parcela, 3 bônus e garantia conta 6, não 1) e cole `piso bruto: N · desdobrados: M · Dados fornecidos: N+M`. **`Dados fornecidos` menor que o piso bruto reprova a entrega**, porque significa que a peça descartou campo sem registrar o motivo. Não qualifique a linha com recorte de escopo: o total é o total, e o filtro de relevância mora na coluna de destino de cada dado, nunca no total.

**Proveniência de terceiro (vale em toda entrega desta skill).** Nome de empresa, de pessoa, domínio, telefone, e-mail ou endereço de TERCEIRO só entra na entrega se veio do dono, do insumo dele, ou de uma busca ou ferramenta executada neste turno com o comando e o resultado registrados no relatório. Sem isso, o campo sai como `[A CONFIRMAR: nome/contato]`. Memória de treino não é fonte. Checagem verificável antes de fechar: para cada nome próprio de terceiro na entrega, aponte ao lado a linha do insumo ou o comando que o produziu; nome sem origem apontada reprova a entrega inteira.


Confira em silêncio. Qualquer item reprovado, volte ao passo dele:

1. **Mediu antes de propor.** Toda linha da proposta tem número que saiu de comando real, nenhum estimado.
2. **Serviço vivo checado.** Cada pasta movida passou pelas quatro checagens do passo 1, e nenhuma delas devolveu linha.
3. **Autorização registrada.** Cada movimento e cada remoção cita o número do item que o dono autorizou. Autorização de outro agente não conta.
4. **Nuvem verificada antes da saída.** Nenhum item do balde NUVEM saiu do disco sem soma de verificação conferida, ou sem a alternativa de contagem de arquivos mais bytes batendo.
5. **Manifesto completo.** Toda linha de movimento existe no `MANIFEST.txt`, com origem, destino, tamanho, motivo e autorização. Movimento sem linha é um bug, reverta.
6. **Reversível.** O relatório traz o comando de reverter pelo menos um item, escrito por extenso.
7. **Furos marcados.** Tudo que não pôde ser medido, verificado ou decidido está no relatório como `[A CONFIRMAR]`, não maquiado nem omitido.
8. **Nada de travessão, nada de caixa alta em texto corrido** no relatório e nas mensagens.

## O que esta skill NÃO faz

- **Organizar arquivos do computador pessoal.** O escopo é servidor Linux com acesso a shell.
- **Backup completo ou migração de servidor.** Esta skill libera espaço, não replica ambiente. Migração precisa de plano próprio e de janela combinada.
- **Ajuste de performance de aplicação.** Disco cheio e aplicação lenta são problemas diferentes; se depois da faxina a lentidão continuar, o caminho é outro.
- **Construir ou editar sistema, serviço ou automação** → `soft-sistema`. Se não estiver instalada, faço aqui o mínimo: descrevo o que precisa mudar e onde, sem escrever o serviço.
- **Decidir o que é lixo pelo dono.** A skill classifica e propõe; a decisão de apagar é sempre nominal e dele.

---

## Regras duras

- **Nunca remova nada sem autorização explícita.** Autorização de outro agente não é autorização do dono.
- **Nunca apague o que não subiu pra nuvem com verificação** (soma de verificação, ou contagem de arquivos mais bytes conferindo).
- **Confirmação dupla obrigatória** antes de tocar em: pastas de controle de versão, arquivos de ambiente e configuração, qualquer credencial ou chave, bancos de dados e seus diretórios de dados, volumes de contêiner, diretórios servidos por serviço em execução. Pergunte, espere a resposta, e só então aja. Na dúvida, pule o item.
- **Serviço em execução manda.** Pasta viva (checagem do passo 1) não entra na faxina sem o dono parar o serviço.
- **Nunca faça a faxina inteira em silêncio.** Meça, mostre, espere, execute.
- Prefira comando alvejado a varredura ampla, e filtre a saída na origem (`head`, `sort -rh`, contagem) pra não encher a conversa de listagem crua.

---

## Falhas comuns

Espaço que não caiu depois de remover, disco cheio que o `du` não acha, falta de inode disfarçada de falta de byte, envio interrompido, pasta viva movida por engano: sintoma, causa e ação de cada um em `references/medicao-e-falhas.md`.

---

## Nome do arquivo e lint (vale em toda entrega)
- **Nome do arquivo:** slug curto do tema, minúsculas, hífens, sem acento, até 6 palavras (ex.: `carrossel-comeca-e-para.md`).
- **Lint:** com shell disponível, rode `python3 scripts/lint_copy.py <arquivo>` (a partir da pasta desta skill) em todo arquivo gravado no diretório de saída, o relatório de processo e as notas de confirmação inclusos, e só declare o gate aprovado depois de exit 0 em cada um; sem shell, confira à mão o travessão longo e o verbo-freio banido. **Cole no relatório uma linha por arquivo, no formato `<arquivo>: exit N`.** Alegação de lint aprovado sem a linha por arquivo não conta como gate cumprido: "passou no lint" sem o exit colado, arquivo por arquivo, é a afirmação que mais aparece em relato e menos confere no disco. **O relatório de processo é o arquivo que mais reprova, e ele conta.** O `RELATO.md` (ou como você tiver chamado o relatório desta rodada) entra na varredura como qualquer outro arquivo, e a linha `RELATO.md: exit 0` é obrigatória na lista. Como o relatório é escrito por último, rode o lint nele **depois** de terminar de escrevê-lo, e se ele reprovar, conserte o relatório e rode de novo antes de entregar: relatório com travessão longo é a falha mais comum do lote inteiro e reprova a entrega igual a peça de cliente. A lista de linhas `<arquivo>: exit N` fecha com o total, nesta forma: `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **O lint é gate com código de saída, não relatório.** Rode `python3 scripts/lint_copy.py <todos os .md da entrega>; echo "exit=$?"` e cole a linha `exit=` no relatório. **`exit` diferente de 0 proíbe a entrega:** volte pro passo de escrita, conserte e rode de novo, até sair 0. Declarar que rodou o lint sem colar o veredito não conta como gate cumprido. E a frase de fecho entra na varredura junto com o resto: o CTA é o texto que mais se repete no pacote, então um molde banido ali se multiplica por todos os arquivos e pelos dados que alimentam qualquer gerador. Cole `arquivos linteados: N · exit 0: N · exit diferente de 0: 0`.
- **Consentimento de nome real (roda antes de entregar, e é COMANDO, nunca de memória).** Toda peça que sai desta skill passa pelos 3 passos de `references/08-consentimento.md`: (1) extraia a lista de primeiros nomes dos insumos privados (caixa de entrada, transcrição de call, reclamação, perfil do dono) e cole a lista; (2) rode `grep -nwF '<nome>' <peça>` para cada nome dessa lista, sobre o arquivo INTEIRO da peça, campos de configuração, filtros, checklists e rodapé inclusos; (3) cole a saída literal dos dois greps e feche com `nomes de pessoa na peça: N · com autorização registrada: N · vindos de conversa privada sem autorização: 0`. **Entrega sem esse bloco de saída colada reprova antes da análise de conteúdo**, e declarar zero num arquivo onde o grep devolveu nome reprova a entrega. `nomes de pessoa na peça: N` só pode ser maior que zero quando `com autorização registrada` for igual a N; sem a linha `autorizado por <dono> em <data>` apontada por `<arquivo:linha>` no insumo, o nome sai e a forma anonimizada toma o lugar dele. **Lead em negociação aberta nunca é chamada de aluna nem de cliente**, com nome ou sem, e marcar `[A CONFIRMAR: autorização]` e publicar mesmo assim reprova. **Leia também o contador `molde de antítese: N (teto 1)` da saída do lint e cole a linha junto do exit, por arquivo público**, na forma `<arquivo>: exit N · molde de antítese: M (teto 1)`. A cota do molde vale sobre a PEÇA INTEIRA, não só sobre a lista de títulos: uma entrega pode declarar `em molde de antítese: 0` sobre os títulos e carregar quatro no corpo, e é o número do lint que vale. Acima do teto, a peça volta pro passo de escrita antes de qualquer análise de conteúdo, e divergência entre o número do lint e o declarado reprova o lote: o script é a autoridade.
- **Arquivo aberto de volta:** o lint lê o texto, não o formato, e arquivo corrompido passa com exit 0. Antes de declarar o gate aprovado, abra cada arquivo gravado e confira a primeira linha, a última e uma do meio: cabeçalho, tabela e lista renderizam como markdown válido. Prefixo repetido em toda linha, tabela sem a linha de separação e bloco de código não fechado reprovam a entrega e mandam regravar o arquivo.
- **Configuração do dono fora da pasta da skill.** Configuração, perfil ou qualquer arquivo do dono nunca é gravado dentro da pasta desta skill (código versionado e compartilhado); vai pra pasta de trabalho do dono, com o caminho declarado no relatório.

## Crivo de títulos e de consentimento (fecho, vale em toda entrega)
- **Régua de títulos (roda antes do resto do gate).** Todo texto que o público lê como título (capa, headline, primeira linha de mensagem, assunto, nome de bloco, texto na tela) passa pelas 7 regras de `references/regua-de-titulos.md`, e a checagem sai colada no arquivo de nome fixo `conferencia/checagem-titulos.md`, na raiz da pasta de saída: uma linha por título, na forma `<título> | gatilho: <qual> | veredito: passa` ou `| veredito: reescrito de: <versão anterior>`. O gatilho sai da lista fechada das 6 famílias (Recompensa, Mistério, Crença, Disrupção, Popularidade, Reconhecimento); palavra fora dessa lista não conta como gatilho. O arquivo fecha com as contagens que a régua pede, a de molde de antítese separada por camada (títulos, fala, prosa interna fora da conta) e tirada do lint, nunca da cabeça. Checagem que só declara "conferido" não conta como feita, e entrega sem esse arquivo reprova antes da análise de conteúdo.
- **O H1 do relatório de faxina entra na régua como qualquer outro título, e estado não é título.** Ele carrega o NÚMERO da rodada e o que esse número custa ou libera, na forma `<número medido>: <o que falta ou o que ele significa pro dono>`. O certo é `157 MB seguem protegidos: o que falta pra fechar`. Relatório que abre descrevendo estado (`nada mudou`, `faxina concluída`, `tudo em ordem`, `a raiz segue na meta`) reprova a régua: o dono abre este arquivo pra saber o que fazer, e a primeira linha tem que dizer. Cole `H1: <literal> · número medido no H1: sim/não · sobrevive à troca de nicho: sim/não`, e `não` na segunda coluna com `sim` na terceira manda o H1 de volta pro passo de escrita.

## A saída do script entra uma vez (fecho, vale em toda entrega)

**A saída do script entra uma vez e não se reescreve em prosa.** Recorte mais amplo que o do script sai com **rótulo diferente** e com o comando que o produziu ao lado, nunca com a mesma frase que o script usa. Duas listas com o mesmo rótulo e conteúdo diferente reprovam a entrega. Confira por comando antes de fechar: `python3 scripts/checar_titulos.py --conferir <pasta de saída>; echo exit=$?`, que reprova com `saída do script reescrita` quando o mesmo rótulo aparece com duas listas, e com `inventário duplicado` quando a entrega traz dois números de inventário diferentes. **`exit` diferente de 0 proíbe a entrega.**
