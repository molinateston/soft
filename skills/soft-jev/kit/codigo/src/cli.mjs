#!/usr/bin/env node
import { checkConfiguration, decide, fallback } from './client.mjs';
import { MAX_REQUEST_BYTES } from './contracts.mjs';

/** @param {unknown} value */
const output = (value) => process.stdout.write(`${JSON.stringify(value)}\n`);

/** @param {number} [limit] @returns {Promise<unknown>} */
async function stdinArguments(limit = MAX_REQUEST_BYTES) {
  const chunks = [];
  let size = 0;
  for await (const chunk of process.stdin) {
    const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    size += bytes.length;
    if (size > limit) {
      process.stdin.destroy();
      throw new Error('invalid_arguments');
    }
    chunks.push(bytes);
  }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'));
}

/** Plain text from stdin for `jev ask --dado -` (bounded like the JSON input). */
async function stdinText() {
  const chunks = [];
  let size = 0;
  for await (const chunk of process.stdin) {
    const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    size += bytes.length;
    if (size > MAX_REQUEST_BYTES) { process.stdin.destroy(); break; }
    chunks.push(bytes);
  }
  return Buffer.concat(chunks).toString('utf8');
}

async function main() {
  const args = process.argv.slice(2);
  if (args[0] === 'ask') {
    // Pergunta fechada no meio do trabalho; erros esperados saem como JSON com exit 0.
    const { runAsk } = await import('./ask.mjs');
    const result = await runAsk(args.slice(1), { stdin: stdinText });
    output(result);
    if (result.reason === 'invalid_arguments') process.exitCode = 2;
  } else if (args.length === 0 || (args.length === 1 && args[0] === '--mcp')) {
    const { startServer } = await import('./server.mjs');
    await startServer();
  } else if (args.length === 1 && args[0] === '--check') {
    output(checkConfiguration());
  } else if (args.length === 1 && args[0] === '--smoke') {
    output(await decide({ state: { document: 'The fictional system is available.' }, questions: {
      is_available: { type: 'noul', instructions: 'Does `document` explicitly say the fictional system is available?' },
    } }));
  } else if (args.length === 1 && args[0] === '--decide') {
    const { decideAndLog } = await import('./decision-log.mjs');
    const { withBands } = await import('./ask.mjs');
    let input;
    try { input = await stdinArguments(); } catch { input = null; }
    output(withBands(await decideAndLog(input, 'cli')));
  } else if (args.length === 1 && args[0] === '--rerank') {
    // Reranking de busca: stdin {pergunta, trechos: [{id, texto}]}; falha devolve a ordem de entrada.
    const { runRerank, RERANK_INPUT_BYTES } = await import('./rerank.mjs');
    let input;
    // Entrada maior que a chamada: os trechos são cortados e mascarados antes; a chamada segue no teto de 24 KB.
    try { input = await stdinArguments(RERANK_INPUT_BYTES); } catch { input = null; }
    output(await runRerank(input));
  } else if (args.length === 1 && args[0] === '--decisions') {
    const { listDecisions } = await import('./decisions.mjs');
    output({ decisions: await listDecisions() });
  } else if (args.length === 2 && args[0] === '--decision') {
    // Inputs come from stdin as a JSON object keyed by the decision's declared inputs.
    const { runDecision } = await import('./decisions.mjs');
    let input;
    try { input = await stdinArguments(); } catch { input = null; }
    const { withBands } = await import('./ask.mjs');
    output(input === null ? { ...fallback('invalid_input'), decision: args[1] } : withBands(await runDecision(args[1], input)));
  } else {
    output(fallback('invalid_arguments'));
    process.exitCode = 2;
  }
}

main().catch(() => {
  // Errors may contain input or credentials. Never print raw Error objects.
  process.stderr.write('JEV initialization failed.\n');
  process.exitCode = 1;
});
