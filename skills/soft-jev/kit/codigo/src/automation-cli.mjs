#!/usr/bin/env node
import { runAutomation, skipped } from './automation.mjs';

async function main() {
  const chunks = [];
  let size = 0;
  for await (const chunk of process.stdin) {
    size += chunk.length;
    if (size > 131_072) { process.stdin.destroy(); throw new Error('oversized'); }
    chunks.push(chunk);
  }
  const result = await runAutomation(JSON.parse(Buffer.concat(chunks).toString('utf8')));
  process.stdout.write(`${JSON.stringify(result)}\n`);
}
main().catch(() => {
  // Raw host input and errors must never be logged.
  process.stdout.write(`${JSON.stringify(skipped('invalid', '', 'invalid_event'))}\n`);
});
