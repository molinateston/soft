# Segurança

Nota fiscal mexe com dinheiro e com o certificado da empresa. Esta página junta onde cada coisa sensível mora, quem pode ver e o que os scripts fazem para que nada vaze.

## Onde cada coisa mora

| O quê | Onde | Permissão |
|---|---|---|
| fichas da empresa e dos clientes | `NFSE_DADOS_DIR/empresa.json` e `NFSE_DADOS_DIR/clientes/` | 600 nos arquivos, 700 na pasta |
| contador do DPS | `NFSE_DADOS_DIR/contador-dps.json`, com cadeado em `.cadeado` | 600 |
| rascunhos | `NFSE_DADOS_DIR/rascunhos/<hash>/` | 600 |
| notas (DPS, DPS assinado, XML autorizado, PDF, estado, resposta) | `NFSE_DADOS_DIR/notas/<ambiente>/<AAAA-MM>/<cliente>-s<série>-dps<número>/` | 600 |
| palavra-passe | `NFSE_DADOS_DIR/palavra-passe.json`, só hash PBKDF2 com sal | 600 |
| registro de auditoria | `NFSE_DADOS_DIR/registro.jsonl`, uma linha por ação, sem segredo | 600 |
| certificado .pfx | `NFSE_PFX_PATH`, numa pasta só do usuário do agente, fora de nuvem | 600 obrigatório |
| senha do certificado | `NFSE_PFX_PASSWORD`, vinda do cofre de segredos ou de variável de ambiente | fora de disco legível |

Os scripts recusam `NFSE_DADOS_DIR` vazia e recusam qualquer caminho de dados, de saída de PDF ou de certificado dentro da pasta da skill. A recusa vem antes de criar qualquer pasta. A pasta da skill vai para pacote público; dado fiscal lá dentro vazaria na próxima publicação.

Pasta de dados com nome de serviço de nuvem (Dropbox, OneDrive, Google Drive, iCloud e parecidos) gera aviso. XML fiscal e registro ficam melhor numa pasta local.

## A senha do certificado

- Entra só por `NFSE_PFX_PASSWORD`. Nunca por argumento de comando (argumento aparece na lista de processos), nunca em arquivo da pasta de dados, nunca na conversa.
- Os scripts nunca imprimem a senha, nem em mensagem de erro. Senha errada sai como "senha errada ou .pfx corrompido", sem eco.
- Se o dono colar a senha na conversa, o agente não usa, diz que ela precisa ir para o cofre e pede para apagar a mensagem.
- A palavra-passe de produção não pode ser igual à senha do certificado; o script recusa.

## O certificado e a chave privada

- O .pfx precisa estar com permissão 600. Com leitura para grupo ou outros, os scripts recusam e mostram o `chmod 600` exato.
- Para a conexão TLS, a chave privada vai para um arquivo temporário numa pasta 0700, com o arquivo 0600 e a chave cifrada por uma senha de uso único que só existe na memória do processo. O contexto TLS carrega o par e, logo em seguida, os arquivos são sobrescritos com zeros e apagados, junto com a pasta, antes de qualquer conexão. O autoteste prova: o arquivo nasce 0600, começa pelo cabeçalho de chave privada cifrada e não existe mais quando a conexão começa.
- Quem quiser o temporário em memória aponta `TMPDIR` para uma pasta em RAM.
- A skill confere se o CNPJ gravado no certificado bate com a ficha e se o certificado está dentro da validade. Faltando 30 dias ou menos, avisa.

## A palavra-passe de produção

- Serve para provar que foi o dono quem mandou emitir em produção, porque a emissão é irreversível. Na produção restrita não é pedida.
- O dono define uma vez com `palavra-passe --definir`, digitando no terminal ou pela entrada padrão. O arquivo guarda só o hash PBKDF2-SHA256 com sal aleatório e 600 mil iterações.
- Em produção, o `emitir` pede a palavra-passe a cada nota, pela entrada padrão (`--palavra-passe-stdin`), nunca por argumento. Palavra errada recusa e fica no registro, sem a palavra.
- O agente pede a palavra-passe ao dono a cada emissão em produção e nunca reaproveita uma palavra dita em mensagem anterior.
- O dono pode desligar a palavra-passe na ficha (`"exigir_palavra_passe": false`). O resumo com confirmação explícita continua obrigatório.

## Portões que impedem nota errada

1. Produção só com `NFSE_AMBIENTE=producao` e a flag `--producao` juntas.
2. O `emitir` só assina o rascunho cujo hash bate com o que o dono confirmou. Rascunho alterado depois do resumo é recusado.
3. Rascunho vale 12 horas e só para o ambiente em que foi preparado.
4. O número do DPS do rascunho precisa ser o próximo livre do contador; rascunho velho ou duplicado é recusado.
5. Envio incerto bloqueia novas emissões no mesmo ambiente até a consulta resolver.
6. Nenhum lote: cada nota passa pelo próprio `preparar`, resumo e confirmação.
7. `NFSE_URL_BASE` só aceita o host oficial de cada ambiente (ou endereço local, só para teste na produção restrita).

## O que o agente nunca faz

- Emitir sem mostrar o resumo e sem o sim explícito do dono.
- Tentar de novo um envio incerto antes de consultar.
- Adivinhar código de tributação, retenção ou regime.
- Instalar dependência sem o dono pedir.
- Apagar XML autorizado.
- Gravar qualquer dado do dono dentro da pasta da skill.
