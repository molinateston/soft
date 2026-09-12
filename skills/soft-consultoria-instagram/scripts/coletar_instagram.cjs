#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

// Token: variavel de ambiente APIFY_TOKEN. Se nao estiver no ambiente, o script le um .env
// local, na ordem: APIFY_ENV_FILE (se definida), .env na pasta desta skill, .env do dir atual.
if (!process.env.APIFY_TOKEN) {
  const candidates = [
    process.env.APIFY_ENV_FILE,
    path.join(__dirname, '..', '.env'),
    path.join(process.cwd(), '.env'),
  ].filter(Boolean);
  const envPath = candidates.find((candidate) => fs.existsSync(candidate));
  if (envPath) {
    for (const line of fs.readFileSync(envPath, 'utf8').split(/\r?\n/)) {
      const match = line.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
      if (!match || process.env[match[1]]) continue;
      process.env[match[1]] = match[2].trim().replace(/^['"]|['"]$/g, '');
    }
  }
}

const [profileUrl, outDir, limitRaw = '30'] = process.argv.slice(2);
const token = process.env.APIFY_TOKEN;
const limit = Number(limitRaw);

if (!profileUrl || !outDir || !token || !Number.isInteger(limit) || limit < 1 || limit > 100) {
  console.error('uso: node coletar_instagram.cjs <url-do-perfil> <pasta-de-saida> [limite 1-100]');
  process.exit(1);
}

fs.mkdirSync(outDir, { recursive: true });
const actor = 'apify~instagram-scraper';

async function api(url, options = {}) {
  const join = url.includes('?') ? '&' : '?';
  const response = await fetch(`${url}${join}token=${encodeURIComponent(token)}`, options);
  if (!response.ok) throw new Error(`coleta HTTP ${response.status}: ${(await response.text()).slice(0, 300)}`);
  return response.json();
}

(async () => {
  const detailsInput = { directUrls: [profileUrl], resultsType: 'details', resultsLimit: 1 };
  const detailsRun = (await api(`https://api.apify.com/v2/acts/${actor}/runs?waitForFinish=300`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(detailsInput)
  })).data;
  if (detailsRun.status !== 'SUCCEEDED') throw new Error(`coleta do perfil terminou em ${detailsRun.status}`);
  const profileItems = await api(`https://api.apify.com/v2/datasets/${detailsRun.defaultDatasetId}/items?clean=true&format=json&limit=1`);
  fs.writeFileSync(path.join(outDir, 'perfil-raw.json'), JSON.stringify(profileItems, null, 2));

  const input = { directUrls: [profileUrl], resultsType: 'posts', resultsLimit: limit, addParentData: false };
  const run = (await api(`https://api.apify.com/v2/acts/${actor}/runs?waitForFinish=300`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(input)
  })).data;
  if (run.status !== 'SUCCEEDED') throw new Error(`coleta terminou em ${run.status}`);
  const items = await api(`https://api.apify.com/v2/datasets/${run.defaultDatasetId}/items?clean=true&format=json&limit=${limit}`);
  fs.writeFileSync(path.join(outDir, 'posts-raw.json'), JSON.stringify(items, null, 2));
  fs.writeFileSync(path.join(outDir, 'recibo.json'), JSON.stringify({
    status: run.status, startedAt: run.startedAt, finishedAt: run.finishedAt,
    profileDatasetId: detailsRun.defaultDatasetId,
    postsDatasetId: run.defaultDatasetId,
    profileUsageTotalUsd: detailsRun.usageTotalUsd ?? null,
    postsUsageTotalUsd: run.usageTotalUsd ?? null,
    collected: items.length
  }, null, 2));
  const summary = items.map((item, index) => ({
    index: index + 1, shortCode: item.shortCode ?? null, url: item.url ?? null,
    type: item.type ?? null, timestamp: item.timestamp ?? null, caption: item.caption ?? '',
    likesCount: item.likesCount ?? null, commentsCount: item.commentsCount ?? null,
    videoViewCount: item.videoViewCount ?? item.videoPlayCount ?? null,
    videoUrl: item.videoUrl ?? null, displayUrl: item.displayUrl ?? null,
    childPosts: Array.isArray(item.childPosts) ? item.childPosts.map(child => ({
      displayUrl: child.displayUrl ?? null, type: child.type ?? null
    })) : []
  }));
  fs.writeFileSync(path.join(outDir, 'posts-resumo.json'), JSON.stringify(summary, null, 2));
  console.log(JSON.stringify({ status: run.status, profileCollected: profileItems.length, postsCollected: items.length }));
})().catch(error => { console.error(error.message); process.exit(1); });
