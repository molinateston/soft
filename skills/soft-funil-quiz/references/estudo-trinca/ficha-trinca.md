sinais não medidos

# Engenharia reversa do funil Treino Trinca

Fonte: https://inlead.digital/desafio-treino-trinca-ll/ . Coleta: 15/10/2026, VPS, Chromium headless executado por Playwright. Caminho usado: shell e navegador real.

Abertura confirmada: HTTP 200, título Treino Trinca. Evidência inicial: `01-entrada.json` e `01-entrada.png`. As capturas `01-tela.png` em diante documentam a navegação efetiva. Não houve desafio de segurança.

Premissa: respostas de teste para observar a interface, sem representar o dono ou uma pessoa real. Idade e preferências são escolhas simuladas. A navegação usou apenas opções do questionário e valores padrão; os campos de identidade ficaram vazios. Algumas escolhas são incoerentes entre si; isso limita conclusões sobre a personalização.

## Percurso comprovado

| Captura | Tela | Ação simulada |
|---|---|---|
| 01-tela.png | SE ESFORÇA NA ACADEMIA, MAS A BARRIGA PARECE NÃO SAIR POR NADA? | Inspeção; sem envio de dados |
| 02-tela.png | Qual é a sua idade? | 35 a 44 anos |
| 03-tela.png | Escolha seu objetivo: | Perder peso |
| 04-tela.png | Queime gordura e ganhe músculos rapidamente! | Continuar |
| 05-tela.png | O que mais pretente alcançar com o Treino Trinca? | Corpo estético e funcional |
| 06-tela.png | O que mais pretente alcançar com o Treino Trinca? | Continuar |
| 07-tela.png | E qual é seu fisico atual? | Magro |
| 08-tela.png | Você já treina? | Sim |
| 09-tela.png | A quanto tempo você treina? | Menos de 1 ano |
| 10-tela.png | Qual é o seu maior desafio hoje? | Treino faz tempo, mas estou longe do corpo que eu gostaria |
| 11-tela.png | Eu te entendo, parceiro... | TAMBÉM QUERO ISSO! |
| 12-tela.png | Qual é o físico que você quer ter? | Magro |
| 13-tela.png | Como é sua rotina dia a dia? | Corrida: Mal tenho tempo pra respirar |
| 14-tela.png | Com que frequência você já treina? | Ainda não treino |
| 15-tela.png | Quanto tempo você consegue dedicar ao treino por dia? | Menos de 30 minutos |
| 16-tela.png | Quais músculos são mais importantes pra você? | Peitoral |
| 17-tela.png | Quais músculos são mais importantes pra você? | Continuar |
| 18-tela.png | Você já conhece a metodologia de Treino Trinca? | Já conheço sim |
| 19-tela.png | Como funciona o Treino Trinca? | Continuar |
| 20-tela.png | Você já tinha visto algo parecido que, com 3 dias por semana, te faz perder gordura e ganhar massa muscular de forma NATURAL? | Primeira vez! |
| 21-tela.png | Agora me diz.. Qual é a sua altura? | cm |
| 22-tela.png | Agora me diz.. Qual é a sua altura? | Continuar |
| 23-tela.png | Qual é seu peso atual? | kg |
| 24-tela.png | Qual é seu peso atual? | Continuar |
| 25-tela.png | E qual peso você deseja atingir em 28 dias? | kg |
| 26-tela.png | E qual peso você deseja atingir em 28 dias? | Continuar |
| 27-tela.png | Tenho certeza que você vai conseguir! | Continuar |
| 28-tela.png | Montando o seu plano personalizado... | Continuar |
| 29-tela.png | Um plano personalizado de 28 dias é tudo que você precisa! | Botão de avanço |
| 30-tela.png | ASSISTA O VÍDEO ABAIXO PARA RECEBER O SEU PROTOCOLO... | GARANTIR MINHA VAGA! |
| percurso.log, AFTER_WAIT após etapa 28 | Resultado intermediário após carregamento | Continuar |
| 30-cta.png | Segundo vídeo com botão de compra liberado | Garantir minha vaga |
| 31-checkout.png | Checkout Lastlink | Aberto pelo link público do DOM; formulário vazio |

As capturas 05/06 e 16/17 registram seleção e avanço no mesmo formulário; 21/22, 23/24 e 25/26 registram confirmação de unidades/valores. Na primeira passagem foram 30 estados capturados no quiz, mais um resultado intermediário documentado em log e o checkout. As demais combinações não foram testadas nessa primeira passagem. Altura e pesos permaneceram nos valores padrão da interface: 180 cm, 70 kg atual e 70 kg desejado. A simulação não representa o dono.

## Ficha de oito campos

1. **Ângulo.** Frustração com esforço na academia e gordura abdominal; desejo de força, aparência e disposição. A entrada e as perguntas posteriores sugerem foco masculino. Isso descreve a mensagem observada, sem comprovar quem compra.
2. **Gancho.** Entrada em forma de pergunta sobre barriga que persiste apesar do esforço. O anúncio de origem e seus primeiros segundos não foram fornecidos. A headline foi observada na página; o anúncio de origem não foi examinado.
3. **Formato.** Quiz em coluna central estreita, fundo branco, azul nos destaques e botões, logotipo, imagens e barra de progresso. Perguntas de escolha única e múltipla alternam com páginas de argumento e uma apresentação em vídeo vertical. Prints 01, 04, 11 e 19.
4. **Estrutura invisível.** Entrada: identificação do problema, promessa de transformação com prazo, nome do método, lista de ganhos e chamada para teste. Telas 02/03: faixa etária e objetivo. Tela 04: associação a celebridades e profissionais ocupados, seguida de redução do esforço percebido. Telas 05 a 10: desejos, situação e dificuldade. Tela 11: narrador se aproxima do visitante, relata frustração e atribui mudança ao método; desloca a explicação da idade/genética para o plano. Telas 12 a 17: futuro desejado, rotina, frequência, tempo e músculos. Tela 18: introdução explícita do método. Tela 19: convite para assistir à explicação. Depois vêm reação ao método, medidas corporais com valores padrão, depoimentos, carregamento, resultado de adequação, comparação de transformação e segundo vídeo com chamada à compra. Esta é a ordem vista, sem afirmar aumento de conversão.
5. **Mecanismo.** O nome exibido é Treino Trinca. A página o apresenta como metodologia americana e treino envolvendo todos os músculos três vezes por semana. A tela 04 acrescenta quarenta minutos e menor esforço. A origem, eficácia, uso por celebridades e efeitos hormonais não foram comprovados nesta coleta.
6. **Oferta.** A entrada promete treino personalizado e plano para redução de gordura e ganho muscular. No checkout público: R$ 37,00 à vista ou até 7 parcelas de R$ 6,16; acesso vitalício, pagamento único, cartão ou Pix. A soma das sete parcelas é R$ 43,12, calculada sobre os valores exibidos. Bônus e garantia não visíveis no checkout. Captura `31-checkout.png` e arquivo `31-checkout.json`. O prazo promocional da entrada e a história de perda de peso são alegações do vendedor, sem verificação independente.
7. **Página e funil.** Entrada pública → quiz com argumentos intercalados → vídeo explicativo → reação ao método → altura/peso/peso desejado → depoimentos → carregamento de plano → resultado que recomenda o método → comparação visual de transformação → segundo vídeo → checkout Lastlink. O resultado intermediário foi visto após o carregamento e seu texto está em `percurso.log`, no registro AFTER_WAIT após a etapa 28. Não há print exclusivo desse resultado. O resultado afirma adequação ao tipo físico; não foi comprovada geração real de treino. A URL permanece a mesma nas telas observadas. O link do checkout estava no DOM da tela 30, sem texto de compra visível naquele momento. O endereço foi primeiro aberto em outra sessão do navegador para inspeção. Depois, na sessão do quiz, o botão Garantir minha vaga surgiu e foi clicado normalmente, levando ao mesmo checkout, conforme o registro CHOICE_AFTER_VIDEO e a URL da etapa 31 em `percurso.log`. O print `30-cta.png` mostra o botão visível. A tela transitória 31-tela.png ficou vazia antes de terminar de carregar; a evidência completa do checkout é 31-checkout.png. O checkout pede e-mail, celular e dados de pagamento. Pagamento, entrega e pós-compra: não visitados. URL: https://lastlink.com/p/CDCF86EC0/checkout-payment/ . HTML inicial contém carregamento de Meta Pixel e UTMify; presença de scripts não comprova eventos corretos, campanhas ativas ou vendas.
8. **Técnica ou personalidade.** Incerto. Há uma pessoa na imagem da capa e no vídeo e há relato pessoal na tela 11, mas faltam dados de audiência e mídia paga para classificar o modelo comercial. Não foi medida verba, duração de anúncios, cópias, conversão ou faturamento.

## Fatos e inferências

Fatos: o navegador abriu, os botões levaram às telas documentadas e o percurso alcançou o segundo vídeo e o checkout público. As perguntas levantam dores, desejos e disponibilidade de tempo; o checkout apresenta os primeiros campos de contato vistos.

Inferência comercial: o questionário também prepara a venda, pois intercala perguntas com argumentos e explicação do método. Perguntas sobre tempo podem preparar uma resposta à objeção de rotina. Não foi comprovado que as respostas mudam o treino entregue ou a oferta final.

A coleta permite descrever a estrutura, mas não sustenta chamar este funil de campeão ou dizer que está escalando.

## Limites e próximo passo

O primeiro vídeo foi iniciado com interação normal. Após verificações espaçadas de 45 segundos, surgiu Continuar e o percurso avançou. O segundo vídeo foi aberto e seu botão de compra apareceu durante a observação, ainda sem transcrição nessa primeira passagem. O player exibe mensagem de saída do ar em breve; não foi comprovado prazo real de disponibilidade. O recurso público do primeiro player foi salvo em `player-publico.js`; sua configuração não comprova duração assistida ou taxa de retenção. Nenhum evento de player foi forçado, nem conteúdo pulado por alteração de tempo.

A borda final foi o formulário de checkout com contato e pagamento. Não preenchi nem enviei esse formulário. Oferta final capturada sem compra. Upsells, área de membros e entrega seguem não visíveis. A continuação audiovisual está documentada abaixo. Para pós-compra faltaria acesso autorizado a material já adquirido, sem realizar compra nesta tarefa.

Não há avaliação clínica ou recomendação de exercícios. As alegações de corpo, hormônios, prazos e transformação foram apenas registradas como mensagem comercial. A skill exclui esse tipo de promessa da modelagem. Nenhuma compra foi feita, nenhum cadastro foi enviado e nenhuma mensagem foi enviada a terceiros.

princípio: hipótese de persuasão pela identificação da dificuldade antes de apresentar uma solução nomeada; efeito em vendas não medido.
modelável: não como peça validada; a ordem entre perguntas e argumentos fica disponível para estudo, com as promessas de saúde e prazo fora de qualquer adaptação.
fica de fora: identidade, imagens, história pessoal, perda de peso alegada, promessas hormonais e de prazo do anunciante.

## Conferência

Gate da ação 3: itens 1 a 9 de Radar/brief não se aplicam; item 10 sim, números são descrição da referência; item 11 sim, sem contorno ou identidade falsa; item 12 comprovado em `prova-validacao.txt`. Sinais de venda continuam não medidos.


## Continuação: vídeos completos e estrutura

Os dois vídeos públicos foram baixados com imagem e áudio a partir das mídias do player já acessível no navegador. O primeiro tem 191,68 segundos, resolução 486 × 720, H.264 e AAC, arquivo video1-720p.mp4. O segundo tem 133,248 segundos, resolução 324 × 480, H.264 e AAC, arquivo original video2-720p.mp4. Esse segundo nome não representa sua resolução; no pacote ele se chama video2-480p.mp4. FFprobe e decodificação completa conferiram as mídias. Não houve instalação ou serviço de transcrição pago.

Transcrições integrais automáticas de estudo: video1-transcricao.txt/json e video2-transcricao.txt/json, geradas com faster-whisper small local. Nomes e algumas palavras estão incertos. Os brutos foram preservados. Mapas em mapa-video1.md e mapa-video2.md cobrem as durações medidas com intervalos contíguos. A análise combina leitura da transcrição e conferência de quadros extraídos; não equivale a revisão humana palavra por palavra do áudio. Os mosaicos mostram as amostras examinadas.

O primeiro vídeo constrói autoridade com alunos, história pessoal, formação, alcance, tempo de aplicação e associação a famosos. Apresenta o problema como inadequação do treino anterior e explica seu mecanismo. O segundo pressupõe essa aceitação e vende o produto: planilha personalizada, vídeos, acompanhamento por equipe no WhatsApp e aplicativo. Essas entregas são promessas narradas, sem comprovação de execução pós-compra.

No segundo vídeo, a oferta passa por referências declaradas de R$500 por hora e R$5 mil mensais no individual; apresenta R$197 e depois R$37 à vista por desconto de lançamento de dez minutos. Declara garantia ampliada de sete para trinta dias e reembolso solicitado no WhatsApp. O checkout confirmou R$37. Os outros preços, expiração da promoção, garantia e atendimento não foram testados. A fala de mudança em 28 dias é alegação comercial, sem avaliação clínica.

Divergências internas: a página relata 43 kg e 44 anos, enquanto a fala transcrita registra 45 kg e 45 anos. Há três treinos por semana em partes da mensagem e três a quatro em outra. Não foi determinada a causa. Eficácia, origem americana e alegações hormonais ou científicas continuam sem verificação independente.

A estrutura proposta em estrutura-reutilizavel.md distingue compra direta de low-ticket e convite para reunião estratégica. É adaptação interna com campos pendentes, sem oferta ou público inventado do dono. A skill pessoal processo-funil-quiz-video foi criada fora do catálogo, sem alterar as skills existentes. A reunião foi incluída por pedido do dono e não é um destino observado neste concorrente.

## Comparação final das sessões novas

Dois percursos novos concluíram a navegação até o destino do checkout. Ver comparacao-perfis.md para escolhas, diferença de pergunta, resultado comum e limite das medidas padrão. A pergunta sobre tempo de prática aparece apenas para quem já treina. Os dois resultados observados e o produto do checkout foram comuns nas condições testadas. Isso não demonstra ausência de personalização em outras combinações ou na entrega após a compra. As capturas finais carregadas do checkout são reaberturas das URLs alcançadas, conforme nota nos respectivos JSONs.
