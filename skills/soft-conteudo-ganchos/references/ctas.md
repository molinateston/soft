# CTA junto com o gancho

CTA é a última linha ou a última lâmina: a ação que a peça pede. Uma peça, um objetivo, um CTA. O banco por objetivo e a regra da palavra do comentário moram na referência única de CTA, `shared-references/cta/`, igual em todas as skills que escrevem CTA:

- `shared-references/cta/cta-01-tipos-e-lugar.md`: os tipos de CTA, onde cada um fica na peça e como medir.
- `shared-references/cta/cta-02-palavra-do-comentario.md`: de onde vem a palavra, as perguntas ao dono, uma por vez, a linha do perfil e a conferência.
- `shared-references/cta/cta-03-textos-base.md`: os moldes por objetivo (seguir, curtir, salvar, enviar, comentar, converter, lâmina do meio e lâmina do fim).

Escolha o molde pelo objetivo que o dono respondeu na pergunta 3 e preencha as lacunas com o que é dele. Cada linha do banco é molde: os colchetes nunca saem no CTA entregue.

## O que vale aqui, quando o CTA sai junto com o gancho

- **`[PALAVRA]` só existe no banco.** No CTA entregue entra a palavra real que a automação do dono já responde, com a linha dela no perfil e a grafia exata, ou o CTA sai na versão sem palavra ("Me chama no direct e eu te mando [recurso]"). Escolher uma palavra aqui é inventar, e palavra sem origem reprova no gate.
- **Comentário puxado por CTA infla a interação.** Não meça a força do gancho pelos comentários de uma peça com pedido de palavra.
- **Todo CTA passa no mesmo gate do gancho**, régua de títulos inclusa: uma frase só, que se explica sem o resto da peça, com o objeto de cada verbo dito e dois gatilhos da lista fechada. Duas frases separadas por ponto gastam a cota de 1 antítese do lote, que o gancho às vezes já usou.
- **O CTA entra no `titulos.txt`** com o gancho, e a linha de conferência da palavra (`palavra-chave: <a palavra> | origem: <arquivo:linha> | recebe: <o que a pessoa recebe>`) vai pra `conferencia/`, nunca pro arquivo do gancho.
