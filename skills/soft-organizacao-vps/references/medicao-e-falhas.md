# Medição fina e falhas comuns

Profundidade do passo 1 (medir) e o diagnóstico de quando a faxina não deu o resultado esperado. O
fluxo do SKILL.md é autossuficiente; este arquivo é o detalhe.

## Alvos clássicos: como medir cada um separado

| Alvo | Como medir |
|---|---|
| Mídia pesada | `find "$RAIZ" -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.mkv' -o -iname '*.zip' -o -iname '*.png' \) -size +20M` |
| Logs | `du -sh /var/log 2>/dev/null` e logs dentro da RAIZ |
| Caches | `du -sh ~/.cache 2>/dev/null`, caches de gerenciador de pacote |
| Dependências reinstaláveis | pastas de dependência de projeto (`node_modules`, `venv`, `vendor`, `target`) |
| Builds e releases antigas | pastas de saída de build, tarballs de versão velha |
| Duplicatas | mesmo tamanho e mesmo nome em pastas diferentes |
| Órfãos | arquivo sem acesso há mais de 180 dias: `find "$RAIZ" -type f -atime +180 -size +50M` |

Se algum comando não existir no ambiente, use o que existir e registre a lacuna no relatório. Nunca
invente número: proposta com tamanho estimado é pior que proposta nenhuma, porque o dono autoriza em
cima de um número que não existe.

## Falhas comuns e o que fazer

| Sintoma | Provável causa | Ação |
|---|---|---|
| Espaço não caiu depois de remover | Processo ainda segura o arquivo aberto | `lsof +L1` e reinicie o serviço dono do arquivo |
| Disco cheio mas `du` não acha | Arquivo apagado ainda aberto, ou outra partição | Compare `df -h` com `du`, cheque partições separadas |
| Muitos arquivos pequenos, disco "cheio" | Falta de inode, não de byte | `df -i`, limpe diretórios com contagem alta |
| Envio pra nuvem interrompido | Rede ou limite do provedor | Repita com retomada, verifique antes de qualquer remoção |
| Pasta some e a aplicação para | Caminho vivo movido sem aviso | Reverta pelo manifesto, deixe o aviso no lugar de origem |
