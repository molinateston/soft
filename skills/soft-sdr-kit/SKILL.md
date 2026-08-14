---
name: soft-sdr-kit
description: O KIT INSTALÁVEL do SDR de IA como PRODUTO, instalar, atualizar, publicar versão e operar o kit em cliente. Âncora, esta skill cuida do PACOTE e da DISTRIBUIÇÃO (página de download, tarball, repo, release, instalação no cliente, troubleshooting de serviço); o MÉTODO comercial (qualificar, vender a sessão, objeção, script) mora na soft-vendas-sdr, e o fechamento na soft-vendas-closer. Use quando o pedido for "instala o SDR no cliente", "kit do SDR", "página de download do SDR", "publica versão nova do kit", "atualiza o SDR do cliente", "o SDR do cliente parou", "manda o SDR pro agente dele", "link de instalação". NÃO use pra escrever script de venda, qualificação ou objeção (soft-vendas-sdr), nem fechamento (soft-vendas-closer), nem pra operar a conta Meta (soft-trafego-meta).
---

# Kit SDR de IA, o produto e a esteira dele

O kit e um SDR de IA marca-neutra que a IA-agente do CLIENTE instala sozinha lendo um manual executavel. Nasce em modo sombra (rascunhos pra aprovacao no topico SDR do Telegram do dono) e so responde lead de verdade com o "pode" escrito do dono. Motor: portas e adapters (trocar CRM = 1 adapter), gate de seguranca em codigo, debounce 8s, killswitch, auditoria por turno, simulador proprio.

## Os 3 enderecos (decorar)

- Pagina de download (sempre a versao atual): `https://licenca.leonardomolina.com.br/sdr`
- Tarball direto (o link NUNCA muda): `https://licenca.leonardomolina.com.br/sdr-kit-v1.tar.gz`
- Oficina (repo privado, fonte da verdade): `molinateston/sdr-kit`, clone canonico em `/root/sdr-kit`

## Instalar num cliente

O dono do kit nao instala nada na mao. A frase que se manda pra IA-agente do cliente:

> Baixa https://licenca.leonardomolina.com.br/sdr-kit-v1.tar.gz , extrai, le o LEIA-PRIMEIRO.md e executa o INSTALAR.md fase por fase.

O agente do cliente conduz as 9 fases do INSTALAR.md: pre-checagem, intake com o dono (perfil de voz + 10 fatos da wiki + token PIT do CRM + agenda), descoberta de pipelines e campos via API, geracao de config e wiki, servico systemd, webhook no CRM (passo a passo sem jargao pro dono), topico SDR no Telegram, simulador verde, sombra de fabrica.

O que o cliente precisa ter na mao: token PIT do GHL (Settings, Private Integrations) + Location ID, e uns 30 minutos pro intake. Cliente sem GHL: o kit e GHL-first; adapter novo e trabalho nosso de oficina (bateria de contrato antes de entrar no kit).

Acompanhar a primeira instalacao de cada cliente no topico dele: o que emperrar vira correcao do kit pra todos os proximos.

## Atualizar um cliente

Mesmo link, mesma frase: o agente dele baixa de novo e aplica por cima seguindo o INSTALAR.md. Regra de ouro em toda atualizacao de motor: simulador verde + restart do servico (`systemctl restart`), nunca subir processo na mao (instancia manual segurando a porta derruba o servico com EADDRINUSE, aconteceu 2x na operacao-mae).

## Publicar versao nova (oficina, so nos)

No clone `/root/sdr-kit`: editar, rodar `cd motor && node bin/simular.cjs` (precisa verde), commit, push, `./publicar.sh`. O publicar.sh e o porteiro: roda o simulador de novo, empacota via git archive do HEAD (so o commitado viaja), publica o tarball e regenera a pagina `/sdr` com data e commit. O link do cliente nunca muda; quem muda e o pacote por tras.

Grep-prova de identidade antes de todo release relevante: o kit nao pode carregar nome, ID de CRM, chat de Telegram ou URL da operacao-mae (doutrina da purga; a regua que ja se provou: `grep -rniE "leonardo|molina|<location>|<pipeline>|<chats>"` no kit deve dar zero).

## Divisao de responsabilidade entre as skills

- Esta skill (soft-sdr-kit): o PACOTE. Distribuicao, instalacao, release, servico, troubleshooting.
- soft-vendas-sdr: o METODO do SDR (qualificar, vender a sessao, prospeccao, playbook). O kit hoje carrega o CORPO (atender, estados, gate, handoff); a infusao do metodo no cerebro por objetivo de funil (agendar = vende a sessao; fechar ate o limiar = conduz ao checkout sozinho) e o proximo trabalho de motor, registrado no plano-mae `/root/PLANO-MAQUINA-SDR.md`.
- soft-vendas-closer: fechamento humano. O kit passa lead quente com briefing; quem fecha acima do limiar e gente.

## Troubleshooting rapido

- Servico caiu ou responde 500: `systemctl status sdr-rascunho` na maquina do cliente; o unit tem Restart=always, se esta em loop ver o log do motor (quase sempre EADDRINUSE de instancia manual, matar a solta e deixar o systemd reassumir).
- Rascunho nao chega no topico: conferir o webhook no CRM (workflow ativo, URL com secret) e o token do bot do Telegram no instalacao.json.
- Gate barrando resposta certa: rodar o simulador; se a regua estiver errada, o conserto e na oficina e sai release novo (nunca remendo local no cliente).
- Lead sem resposta e sem aviso: ver killswitch (arquivo de pausa) e o monitor no cron.

## Backlog de motor (minerado de benchmark, nao perder)

1. Camada de ETAPA DA CONVERSA alem do estado do lead (o SalesGPT roda um classificador de estagio comercial por turno: abertura, qualificacao, proposta de valor, objecao, fechamento). E o encaixe natural da infusao do metodo soft-vendas-sdr.
2. Extracao estruturada POR TURNO de BANT, compromissos e objecoes do lead, persistida por contato (o template B2B da OpenClaw faz isso e o briefing de handoff fica pronto sozinho).
3. Bateria de contrato de adapter (todo CRM novo passa a mesma suite antes de entrar no kit).
