// News image v2 for Monday 23 November 2026 (make.fun news-image-20261123).
// The front page is drawn by compose.py at build time and stored in this
// repo as entry.png; this loader validates it and copies it to /output.
// Node 22, standard library only, no network access.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const LIMIT_BYTES = 1024 * 1024;
const EXPECTED_SIDE = 1024;

function abort(reason: string): never {
  console.error(`news-image-20261123 v2: ${reason}`);
  process.exit(1);
}

function inspectPng(bytes: Buffer): { width: number; height: number } {
  if (bytes.length > LIMIT_BYTES) {
    abort(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
  }
  if (bytes.length < 45) {
    abort("entry.png is too short to hold a PNG header and trailer");
  }
  if (!bytes.subarray(0, 8).equals(SIGNATURE)) {
    abort("entry.png does not start with the PNG signature");
  }
  if (bytes.toString("latin1", 12, 16) !== "IHDR") {
    abort("entry.png has no IHDR chunk where one belongs");
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width !== EXPECTED_SIDE || height !== EXPECTED_SIDE) {
    abort(`entry.png is ${width}x${height}, expected 1024x1024`);
  }
  if (bytes.toString("latin1", bytes.length - 8, bytes.length - 4) !== "IEND") {
    abort("entry.png ends without the IEND chunk");
  }
  return { width, height };
}

function checkCanvas(bytes: Buffer): void {
  if (bytes.length === 0) {
    abort("entry.png is empty, there is nothing to copy");
  }
  const chunkLength = bytes.readUInt32BE(8);
  if (chunkLength !== 13) {
    abort(`IHDR chunk declares ${chunkLength} bytes, expected 13`);
  }
  const canvasWidth = bytes.readUInt32BE(16);
  const canvasHeight = bytes.readUInt32BE(20);
  if (canvasWidth !== EXPECTED_SIDE) {
    abort(`entry.png is ${canvasWidth} pixels wide, the page must be 1024`);
  }
  if (canvasHeight !== EXPECTED_SIDE) {
    abort(`entry.png is ${canvasHeight} pixels tall, the page must be 1024`);
  }
  const bitDepth = bytes[24];
  const colourType = bytes[25];
  if (bitDepth !== 8) {
    abort(`entry.png has ${bitDepth}-bit samples, expected 8-bit`);
  }
  if (colourType !== 2 && colourType !== 6) {
    abort(`entry.png colour type ${colourType} is not truecolour`);
  }
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");
  if (!existsSync(source)) {
    abort("entry.png is missing from the repo");
  }
  const bytes = readFileSync(source);
  const { width, height } = inspectPng(bytes);
  checkCanvas(bytes);

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  // The bytes are copied unchanged, so repeated runs stay identical.
  writeFileSync(join(outDir, "entry.png"), bytes);
  console.log(`wrote entry.png (${bytes.length} bytes, ${width}x${height})`);
}

main();
