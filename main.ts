// Entry program for the gta6-meme-x-01 bounty (Node 22, standard library only).
//
// The entry is the X post itself: a Leonida County Court verdict finding
// Rockstar Games guilty of thirteen years of aggravated waiting. This
// program has exactly one job — carry POST.json, the posted meme's address,
// from the repository into the output directory where the gate can read it.
//
// POST.json starts as a placeholder. After the meme is posted on X, the real
// post address replaces the placeholder and this program is run again; the
// gate then fetches the post itself. Nothing this program prints is judged.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const POST_FILE = "POST.json";

// An X post address is https://x.com/<handle>/status/<digits> (twitter.com
// works too). Anything else is a placeholder that has not been filled in yet.
function isPostAddress(value: unknown): value is string {
  if (typeof value !== "string") return false;
  let parsed: URL;
  try {
    parsed = new URL(value);
  } catch {
    return false;
  }
  const hostOk = parsed.hostname === "x.com" ||
    parsed.hostname === "twitter.com" ||
    parsed.hostname.endsWith(".x.com") ||
    parsed.hostname.endsWith(".twitter.com");
  if (!hostOk || parsed.protocol !== "https:") return false;
  const parts = parsed.pathname.split("/").filter(Boolean);
  return parts.length === 3 && parts[1] === "status" && /^\d+$/.test(parts[2]);
}

function readPostAddress(): string {
  const source = join(botDir, POST_FILE);
  if (!existsSync(source)) {
    console.error(`no ${POST_FILE} found in ${botDir}; cannot hand off a post`);
    process.exit(1);
  }
  let raw: string;
  try {
    raw = readFileSync(source, "utf8");
  } catch (err) {
    console.error(`could not read ${source}: ${(err as Error).message}`);
    process.exit(1);
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    console.error(`${POST_FILE} is not valid JSON: ${(err as Error).message}`);
    process.exit(1);
  }
  const url = (parsed as { url?: unknown }).url;
  if (!isPostAddress(url)) {
    console.error(
      `${POST_FILE} has no posted address yet (expected ` +
        `https://x.com/<handle>/status/<id>); post the meme first, ` +
        `then replace the placeholder and run again.`,
    );
    process.exit(1);
  }
  return url;
}

function main(): void {
  const url = readPostAddress();
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, POST_FILE);
  try {
    writeFileSync(target, JSON.stringify({ url }) + "\n");
  } catch (err) {
    console.error(`could not write ${target}: ${(err as Error).message}`);
    process.exit(1);
  }
  console.log(`handing off post: ${url}`);
}

main();
