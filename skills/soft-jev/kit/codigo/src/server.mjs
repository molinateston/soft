import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { fallback } from './client.mjs';
import { decideAndLog } from './decision-log.mjs';
import { withBands } from './ask.mjs';
import { INPUT_SCHEMA } from './contracts.mjs';

export async function startServer() {
  const server = new Server({ name: 'jev-auto', version: '0.1.0' }, { capabilities: { tools: {} } });
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [{
      name: 'jev_decide',
      description: 'Advisory closed semantic decisions: choice, yes/no probability (noul), rubric score. Call it on your own in the middle of a task when a closed decision comes up (did this test result pass? which of these files covers X? does this text make a forbidden promise? error or just a warning?); not for open decisions or anything a command can verify. Batch up to 16 independent questions over minimal non-sensitive state (24 KB total). Sends only these inputs to TypeSafe. Never use for authorization, secrets, generation or simple arithmetic. Each answer comes with `faixas[id]`: alta (≥ 0.8) follow it; media (0.6-0.8) check another way; baixa (< 0.6 or an abstain option) decide yourself. If unavailable, continue normal reasoning. This call may use separately billed TypeSafe tokens.',
      inputSchema: /** @type {import('@modelcontextprotocol/sdk/types.js').Tool['inputSchema']} */ (INPUT_SCHEMA),
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: false, openWorldHint: true },
    }],
  }));
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const result = request.params.name === 'jev_decide' ? withBands(await decideAndLog(request.params.arguments, 'mcp')) : fallback('unknown_tool');
    return { content: [{ type: 'text', text: JSON.stringify(result) }], structuredContent: result, isError: false };
  });
  // The SDK may provide errors containing user input. Keep stdio exclusively for MCP.
  server.onerror = () => {};
  await server.connect(new StdioServerTransport());
  return server;
}
