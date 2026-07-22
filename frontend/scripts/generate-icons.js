import sharp from "sharp";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(__dirname, "..", "public");
const iconsDir = path.join(publicDir, "icons");

const cibles = [
  { source: "icon.svg", sortie: "icon-192.png", taille: 192 },
  { source: "icon.svg", sortie: "icon-512.png", taille: 512 },
  { source: "icon-maskable.svg", sortie: "icon-192-maskable.png", taille: 192 },
  { source: "icon-maskable.svg", sortie: "icon-512-maskable.png", taille: 512 },
];

async function run() {
  for (const { source, sortie, taille } of cibles) {
    await sharp(path.join(iconsDir, source))
      .resize(taille, taille)
      .png()
      .toFile(path.join(iconsDir, sortie));
    console.log(`✓ icons/${sortie}`);
  }

  await sharp(path.join(iconsDir, "icon.svg"))
    .resize(180, 180)
    .png()
    .toFile(path.join(publicDir, "apple-touch-icon.png"));
  console.log("✓ apple-touch-icon.png");
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
