# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Caminhos, tamanhos, nomes de pasta e saídas de comando foram
> inventados só pra mostrar a FORMA de cada etapa. Nenhum número daqui pode ser copiado pra uma
> faxina de verdade: numa faxina real, todo número sai de comando rodado no servidor do dono, e o
> que não pôde ser medido nasce marcado `[A CONFIRMAR]`.

**O caso fictício:** um estúdio de edição de vídeo de 4 pessoas mantém um servidor onde os editores
largam material bruto, renders e projetos. O disco chegou a 87% e o aviso de espaço começou a
aparecer. O dono fictício não é técnico e tem medo de perder material de cliente.

Este arquivo mostra a faxina inteira, na ordem, mais uma reversão de verdade e uma revisão de
quarentena um mês depois.


## Índice

- Passo 0 · A raiz e a nuvem
- Passo 1 · Medir, e a checagem de serviço vivo
- Passo 2 · Classificar em 4 baldes
- Passo 3 · A proposta que o dono aprovou por número
- O mesmo caso, em modo simulação
- Passo 4 · Nuvem, com verificação antes da saída
- Passo 5 · O manifesto preenchido
- Passo 6 · Apagar, os dois itens nominais
- Passo 7 · O relatório
- Uma reversão de verdade, três dias depois
- Revisão de quarentena, um mês depois

---

## Passo 0 · A raiz e a nuvem

**O que o dono deu:**

> "O disco tá cheio, tá dando erro pra salvar render. Dá uma limpada aí, mas pelo amor de deus não
> some com material de cliente."

**A pergunta que a skill fez** (uma mensagem só, duas perguntas dentro):

> Antes de olhar qualquer coisa, preciso de duas respostas:
>
> 1. Qual a pasta a partir da qual eu posso olhar e mexer? (a raiz da faxina)
> 2. Tem nuvem conectada nesse servidor? Se você não souber, eu descubro sozinho.

**Respostas:** raiz `/srv/estudio`. Nuvem: "acho que tem alguma coisa, o rapaz que montou configurou".

Contrato registrado no topo do relatório: **RAIZ = /srv/estudio · nuvem a descobrir no passo 4**.

---

## Passo 1 · Medir (nada mudou no disco)

```
$ df -h /srv
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       197G  172G   16G  92% /

$ du -h -d 2 /srv/estudio | sort -rh | head -8
172G    /srv/estudio
 61G    /srv/estudio/bruto
 34G    /srv/estudio/renders
 28G    /srv/estudio/gravacoes
 19G    /srv/estudio/projetos
 12G    /srv/estudio/app
9,1G    /srv/estudio/projeto-parado-x
3,2G    /srv/estudio/app/build-antigo
```

Tabela do passo 1, do jeito que ela sai:

| Item | Tamanho | Último acesso | Observação |
|---|---|---|---|
| `bruto/2024/` | 38 GB | há 11 meses | material bruto de projetos entregues |
| `bruto/2026/` | 23 GB | há 2 dias | projeto em edição agora |
| `renders/entregas-antigas/` | 13 GB | há 5 meses | render final, já entregue ao cliente |
| `renders/em-curso/` | 21 GB | há 1 dia | render do projeto ativo |
| `gravacoes/2025/` | 28 GB | há 8 meses | bruto de 2025, arquivo morto |
| `projeto-parado-x/` | 9,1 GB | há 1 ano | ninguém sabe o que é |
| `app/build-antigo/` | 3,2 GB | há 4 meses | substituído pela versão 4.1 |
| `app/` (sem o build) | 8,8 GB | agora | aplicação de aprovação de cliente, em uso |
| cache do gerenciador de pacote | 14 GB | contínuo | reproduzível |
| logs rotacionados > 90 dias | 8 GB | contínuo | já comprimidos |
| `projetos/` | 19 GB | há 3 dias | arquivos de projeto do editor, pequenos e vivos |

### A checagem de serviço vivo, rodada pasta por pasta

Em `/srv/estudio/app`, a checagem devolveu linha:

```
$ lsof +D /srv/estudio/app 2>/dev/null | awk 'NR>1{print $1, $2}' | sort -u
node 3312
node 3319

$ grep -rl "/srv/estudio/app" /etc/systemd/system /lib/systemd/system 2>/dev/null
/etc/systemd/system/aprovacao.service
```

Resultado: **`app/` é VIVA**. Vai pro balde FICA como `FICA (serviço ativo: aprovacao.service)`, e
nenhuma proposta toca nela. O `app/build-antigo/` foi checado separado e voltou vazio nas quatro
checagens, então ele sim é candidato.

Nas demais pastas candidatas, as quatro checagens voltaram vazias.

---

## Passo 2 · Classificar em 4 baldes

| Item | Tamanho | Balde | Motivo (uma linha) |
|---|---|---|---|
| `gravacoes/2025/` | 28 GB | NUVEM | pesado, insubstituível, sem leitura há 8 meses |
| `renders/entregas-antigas/` | 13 GB | NUVEM | entrega final de cliente, precisa existir mas não no disco |
| `bruto/2024/` | 38 GB | NUVEM | bruto de projeto entregue, o cliente pode pedir de volta |
| `projeto-parado-x/` | 9,1 GB | QUARENTENA | origem desconhecida, ninguém do time reconhece |
| `app/build-antigo/` | 3,2 GB | QUARENTENA | substituído pela 4.1, mas é o ponto de retorno se a 4.1 falhar |
| cache do gerenciador | 14 GB | APAGA | reproduzível, reinstala sozinho |
| logs > 90 dias | 8 GB | APAGA | rotacionados e comprimidos, já cumpriram a função |
| `app/` | 8,8 GB | FICA | serviço ativo, checagem devolveu processo e unidade |
| `bruto/2026/`, `renders/em-curso/`, `projetos/` | 63 GB | FICA | projeto em edição agora |

Duas decisões que mostram a régua:

- `bruto/2024/` é o maior item da lista, e mesmo assim não foi pra APAGA. Grande e insubstituível vai
  pra NUVEM, nunca pra remoção.
- `projeto-parado-x/` poderia parecer lixo óbvio, mas ninguém soube explicar o que era. Na dúvida
  entre dois baldes, vence o mais conservador: QUARENTENA.

---

## Passo 3 · A proposta que o dono aprovou por número

```
Uso atual: 92% (172G de 197G) · meta sugerida: abaixo de 70%

NUVEM (sobe, verifica, e só então sai do disco)  ..........  79 GB
  1. bruto/2024/                38 GB   último acesso há 11 meses
  2. gravacoes/2025/            28 GB   último acesso há 8 meses
  3. renders/entregas-antigas/  13 GB   último acesso há 5 meses

QUARENTENA (move, apaga só depois de 30 dias)  ............  12 GB
  4. projeto-parado-x/          9,1 GB  sem alteração há 1 ano, origem desconhecida
  5. app/build-antigo/          3,2 GB  substituído pela versão 4.1

APAGA (reproduzível)  .....................................  22 GB
  6. cache do gerenciador de pacote  14 GB   reinstala sozinho
  7. logs rotacionados > 90 dias      8 GB   já comprimidos

FICA (não toco)
  app/ (serviço aprovacao.service ativo), bruto/2026/, renders/em-curso/, projetos/

Total previsto liberado: 113 GB  ·  uso final estimado: 30%

Responda os NÚMEROS que autoriza (exemplo: "1, 2, 5"). O que não for citado, não acontece.
```

**Resposta do dono:** "1, 2, 3, 5, 6, 7. O 4 não mexe, quero olhar antes."

Leitura: o item 4 sai da faxina de hoje e vira linha do relatório. Ninguém insiste.

---

## O mesmo caso, em modo simulação

Se o pedido tivesse sido "simula primeiro", a saída pararia aqui, assim:

```
SIMULAÇÃO, nada foi executado. Nenhum arquivo saiu do lugar.

Item 1 · bruto/2024/   38 GB
  faria: subir pra nuvem, verificar por sha256, depois mover pra
         /srv/estudio/_ARQUIVO/2026-08-07-faxina/midia/bruto-2024/
  reverteria com: mv "/srv/estudio/_ARQUIVO/2026-08-07-faxina/midia/bruto-2024" "/srv/estudio/bruto/2024"
  serviço vivo: nenhum (lsof, systemd, ps e findmnt vazios)

Item 6 · cache do gerenciador de pacote   14 GB
  faria: remoção direta, com sua autorização nominal
  reverteria com: nada, é reproduzível
  serviço vivo: nenhum

Total que sairia do disco: 113 GB · uso final estimado: 30% (hoje 92%)
Itens que a simulação NÃO tocaria: app/ (serviço aprovacao.service ativo)
```

---

## Passo 4 · Nuvem, com verificação antes da saída

Descoberta do conector:

```
$ command -v rclone gdrive aws gcloud az rsync scp 2>/dev/null
/usr/bin/rclone
/usr/bin/rsync
/usr/bin/scp
```

Subida do item 2, e a verificação que autoriza o original a sair:

```
$ rclone copy /srv/estudio/gravacoes/2025 arquivo:estudio/gravacoes-2025 --checksum
Transferred: 28.114 GiB / 28.114 GiB, 100%, 41 files

$ find /srv/estudio/gravacoes/2025 -type f -exec sha256sum {} \; | awk '{print $1}' | sort > /tmp/origem.sha
$ rclone hashsum sha256 arquivo:estudio/gravacoes-2025 | awk '{print $1}' | sort > /tmp/destino.sha
$ diff /tmp/origem.sha /tmp/destino.sha && echo "IGUAL, pode remover a origem"
IGUAL, pode remover a origem
```

Os três itens de NUVEM passaram. Nenhum foi apagado: cada um foi pra quarentena com a nota de onde a
cópia está, porque movimento é reversível e remoção não.

**Se o conector não existisse**, a saída seria um `SUBIR-PRA-NUVEM.md` na raiz, com os três caminhos,
os tamanhos e o comando pronto, e os 79 GB virariam pendência declarada no relatório. Nada seria
apagado por falta de destino.

---

## Passo 5 · O manifesto preenchido

Arquivo `/srv/estudio/_ARQUIVO/2026-08-07-faxina/MANIFEST.txt`:

```
# MANIFEST da rodada 2026-08-07-faxina · raiz: /srv/estudio · prazo: vence em 2026-09-06
# data|origem|destino|tamanho|motivo|autorizacao
2026-08-07|/srv/estudio/bruto/2024|/srv/estudio/_ARQUIVO/2026-08-07-faxina/midia/bruto-2024|38G|balde NUVEM, copiado e verificado por sha256 em arquivo:estudio/bruto-2024|dono autorizou item 1
2026-08-07|/srv/estudio/gravacoes/2025|/srv/estudio/_ARQUIVO/2026-08-07-faxina/midia/gravacoes-2025|28G|balde NUVEM, copiado e verificado por sha256 em arquivo:estudio/gravacoes-2025|dono autorizou item 2
2026-08-07|/srv/estudio/renders/entregas-antigas|/srv/estudio/_ARQUIVO/2026-08-07-faxina/midia/renders-entregas-antigas|13G|balde NUVEM, copiado e verificado por sha256 em arquivo:estudio/renders-2025|dono autorizou item 3
2026-08-07|/srv/estudio/app/build-antigo|/srv/estudio/_ARQUIVO/2026-08-07-faxina/builds/build-antigo|3,2G|balde QUARENTENA, substituido pela versao 4.1|dono autorizou item 5
```

Quatro linhas, quatro movimentos. O item 4 não tem linha porque o dono não autorizou, e por isso ele
continua exatamente onde estava.

---

## Passo 6 · Apagar, os dois itens nominais

Só os itens 6 e 7, citados por número pelo dono:

```
$ du -sh /var/cache/pacote ; ls /var/cache/pacote | wc -l
14G     /var/cache/pacote
2841

$ # confirmação final antes de remover, item por vez
```

Removidos um por vez, nomeados. Nenhuma varredura, nenhum curinga solto. Os itens de quarentena não
foram tocados: o prazo deles vence em 06/09.

---

## Passo 7 · O relatório

Arquivo `/srv/estudio/faxina-2026-08-07.md`:

```markdown
# Faxina 2026-08-07 · /srv/estudio

## Números
- Antes: 172 GB de 197 GB (92%)
- Depois: 59 GB de 197 GB (30%)
- Liberado: 113 GB · meta era abaixo de 70%, ficou em 30%

## Subiu pra nuvem (verificado por sha256, original em quarentena)
| Origem | Destino | Tamanho | Verificação |
|---|---|---|---|
| bruto/2024/ | arquivo:estudio/bruto-2024 | 38 GB | sha256 idêntico, 112 arquivos |
| gravacoes/2025/ | arquivo:estudio/gravacoes-2025 | 28 GB | sha256 idêntico, 41 arquivos |
| renders/entregas-antigas/ | arquivo:estudio/renders-2025 | 13 GB | sha256 idêntico, 68 arquivos |

## Foi pra quarentena
Pasta: _ARQUIVO/2026-08-07-faxina/ · 4 itens · 82,2 GB · prazo vence em 2026-09-06

## Foi apagado
- cache do gerenciador de pacote, 14 GB, autorizado nominalmente (item 6)
- logs rotacionados > 90 dias, 8 GB, autorizado nominalmente (item 7)

## Não foi tocado, e por quê
- app/ · serviço aprovacao.service ativo, checagem devolveu processo 3312 e a unidade
- projeto-parado-x/ (9,1 GB) · você pediu pra olhar antes. Continua no lugar original
- bruto/2026/, renders/em-curso/, projetos/ · projeto em edição agora

## Como reverter
Abra _ARQUIVO/2026-08-07-faxina/MANIFEST.txt, ache a linha, e desfaça exatamente ela:
    mv "/srv/estudio/_ARQUIVO/2026-08-07-faxina/midia/gravacoes-2025" "/srv/estudio/gravacoes/2025"
```

---

## Uma reversão de verdade, três dias depois

> "Preciso do bruto de 2024, o cliente pediu uma versão nova."

A skill abriu o manifesto, achou a linha do item 1, e desfez exatamente ela:

```
$ grep 'bruto/2024' /srv/estudio/_ARQUIVO/2026-08-07-faxina/MANIFEST.txt
2026-08-07|/srv/estudio/bruto/2024|/srv/estudio/_ARQUIVO/2026-08-07-faxina/midia/bruto-2024|38G|...

$ mv "/srv/estudio/_ARQUIVO/2026-08-07-faxina/midia/bruto-2024" "/srv/estudio/bruto/2024"
$ du -sh /srv/estudio/bruto/2024
38G     /srv/estudio/bruto/2024
```

E a linha do manifesto virou:

```
2026-08-07|/srv/estudio/bruto/2024|...|38G|...|dono autorizou item 1
# REVERTIDO em 2026-08-10 a pedido do dono, voltou pra origem
```

A linha original não foi apagada. O histórico é o que prova o que aconteceu.

---

## Revisão de quarentena, um mês depois

```
$ # rodada da varredura de quarentenas
2026-08-07-faxina | 44G | 3 itens | 34 dias | VENCIDA
2026-07-02-faxina | 6,4G | sem manifesto | 70 dias | VENCIDA
```

Duas rodadas vencidas, tratamento diferente para cada uma:

```
QUARENTENA VENCIDA · rodada 2026-08-07-faxina (34 dias, prazo era 30)

  1. gravacoes-2025/      28 GB   já tem cópia conferida no bucket (sha256)
  2. renders-entregas-antigas/  13 GB   já tem cópia conferida no bucket (sha256)
  3. build-antigo/        3,2 GB  ponto de retorno da versão 4.0, a 4.1 está de pé há 34 dias

QUARENTENA VENCIDA · rodada 2026-07-02-faxina (70 dias)
  Sem MANIFEST.txt. Não sei o que foi movido nem de onde veio, então não proponho remoção:
  precisa de decisão sua item a item. Posso listar o conteúdo dela pra você olhar.

Responda os NÚMEROS que autoriza remover. O que não for citado, continua onde está.
```

**Resposta do dono:** "1 e 2 pode. O 3 segura mais um mês."

O que aconteceu:

- Itens 1 e 2 removidos pelo passo 6, um por vez, e as linhas do manifesto marcadas
  `# REMOVIDO em 2026-09-10, autorizado por: dono`, sem apagar a linha.
- Item 3 ficou. O `README.md` da rodada ganhou a linha "prazo estendido a pedido do dono em
  2026-09-10, nova data: 2026-10-10".
- Rodada de julho virou pendência, com o conteúdo listado para o dono decidir depois.
- Relatório `revisao-quarentena-2026-09-10.md` gravado na raiz, com os números do antes e depois.
