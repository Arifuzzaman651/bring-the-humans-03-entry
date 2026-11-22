// bring-the-humans-03 entry (Node 22, standard library only).
//
// The entry is the video itself: an original 20-second vertical ad for
// make.fun, posted publicly on TikTok, whose views decide the places.
// This program only hands in VIDEO.json: it copies it from the repository
// root to /output/VIDEO.json, where the gate reads the video's address.
// Nothing else this program writes is scored.
//
// Outside the grader, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in
// for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// Guard: refuse a placeholder or a non-video address before copying, so a
// bad VIDEO.json fails loudly here instead of passing the gate as invalid.
const source = join(BOT_DIR, 'VIDEO.json');
const parsed = JSON.parse(readFileSync(source, 'utf8')) as { url?: unknown };
const url = typeof parsed.url === 'string' ? parsed.url : '';
if (!/^https:\/\/(www\.|m\.)?tiktok\.com\/@[^/]+\/video\/\d+/.test(url)) {
  console.error(`VIDEO.json does not hold a TikTok video address: ${url || '(none)'}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(source, join(OUTPUT_DIR, 'VIDEO.json'));
console.log('VIDEO.json copied to', join(OUTPUT_DIR, 'VIDEO.json'));
