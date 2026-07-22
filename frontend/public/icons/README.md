# Icônes PWA — génération des PNG

Les fichiers `icon.svg` (maître) et `icon-maskable.svg` (safe zone Android) sont les
sources vectorielles. Les PNG sont générés à partir de ces fichiers — ne pas les
éditer à la main, régénérer depuis les SVG en cas de changement de design.

## Option 1 — `make icons` (recommandé)

Depuis `frontend/` :

```bash
make icons
```

Utilise le script Node `scripts/generate-icons.js` (dépendance `sharp`, déjà dans
`devDependencies`).

## Option 2 — rsvg-convert

```bash
rsvg-convert -w 192 -h 192 icons/icon.svg -o icons/icon-192.png
rsvg-convert -w 512 -h 512 icons/icon.svg -o icons/icon-512.png
rsvg-convert -w 192 -h 192 icons/icon-maskable.svg -o icons/icon-192-maskable.png
rsvg-convert -w 512 -h 512 icons/icon-maskable.svg -o icons/icon-512-maskable.png
rsvg-convert -w 180 -h 180 icons/icon.svg -o apple-touch-icon.png
```

## Option 3 — outil en ligne

Importer `icon.svg` sur un convertisseur SVG→PNG (ex. cloudconvert.com) et exporter
aux tailles 192×192, 512×512 (+ variante maskable), 180×180 pour
`apple-touch-icon.png`.

## Fichiers attendus

| Fichier | Taille | Source |
|---|---|---|
| `icons/icon-192.png` | 192×192 | `icon.svg` |
| `icons/icon-512.png` | 512×512 | `icon.svg` |
| `icons/icon-192-maskable.png` | 192×192 | `icon-maskable.svg` |
| `icons/icon-512-maskable.png` | 512×512 | `icon-maskable.svg` |
| `apple-touch-icon.png` (racine `public/`) | 180×180 | `icon.svg` |
