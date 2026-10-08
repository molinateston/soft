# Se algo der errado

| Sintoma | Causa e conserto |
|---|---|
| Mapa quase vazio | Faltam conceitos. Rode `sugere.py`, escolha as palavras que se repetem e ponha no config. |
| Tudo ligado em tudo | Alguma regex está genérica demais. Troque por uma palavra mais específica. |
| Rótulo sem acento | Escreva o título com `# Título` na primeira linha da nota, ou acrescente a palavra em `acentos`. |
| Pasta não aparece | Confira o `caminho`: é relativo à `raiz`. `*.md` pega só a pasta raiz, `arquivo/*.md` pega a subpasta. |
| `o conceito aponta para o hub ... que não existe` | O `id` do núcleo está escrito diferente em algum lugar do config. |
| `testa.sh` diz "não achei Chrome" | Instale Chrome ou Chromium, ou rode `CHROME_BIN=/caminho/do/chrome bash scripts/testa.sh ...`. Sem navegador, abra o `index.html` à mão e olhe. |
| `testa.sh` falha com Chromium em snap | O snap não lê arquivos fora do home. Copie o `index.html` para dentro do home ou use outro Chrome. |
| `confere.py` acusa link quebrado | A nota citada em `[[...]]` não existe. Crie a nota ou corrija o nome. |
| `confere.py` acusa segredo | Tire a senha, chave ou documento da nota e guarde só o fato ("a chave fica no cofre X"). |
| Nota órfã no aviso do `monta.py` | A nota não tem `[[link]]` nem palavra de conceito. Ligue a uma nota relacionada. |
| O agente não consulta o cérebro | A regra de gravar na hora não está no arquivo de instruções do projeto. Rode `inicia.py --grava-claude-md`. |
