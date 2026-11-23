// News image for Monday 23 November 2026 (make.fun news-image-20261123).
// The front page is drawn by compose.py at build time and stored in this
// repo as entry.png; this loader checks it and writes it to /output.
// Node 22, standard library only, no network.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const MAX_BYTES = 1024 * 1024;

function fail(msg) {
  console.error(`news-image-20261123: ${msg}`);
  process.exit(1);
}

const root = dirname(fileURLToPath(import.meta.url));
const image = readFileSync(join(root, "entry.png"));

if (image.length > MAX_BYTES) {
  fail(`entry.png is ${image.length} bytes, over the 1 MiB limit`);
}
if (image.length < 33) {
  fail("entry.png is too short to be a whole PNG");
}
for (let i = 0; i < PNG_MAGIC.length; i++) {
  if (image[i] !== PNG_MAGIC[i]) fail("entry.png lacks the PNG signature");
}
if (image.toString("latin1", 12, 16) !== "IHDR") {
  fail("entry.png has no IHDR chunk");
}
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`entry.png is ${width}x${height}, expected 1024x1024`);
}
if (image.toString("latin1", image.length - 8, image.length - 4) !== "IEND") {
  fail("entry.png has no IEND chunk");
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
// The bytes are written unchanged, so two runs produce identical output.
writeFileSync(join(outDir, "entry.png"), image);
console.log(`wrote entry.png (${image.length} bytes, 1024x1024)`);
