// Copy into <project>/scripts/ and list every path the build reads from disk.
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const required = [
  'assets-src/credits.json',
  'credits.template.html',
  'assets/jayson.jpg',
  'assets-src/raw/duluth-bridge-night.jpg',
  'assets-src/raw/lake-superior-dawn.jpg',
  'assets-src/raw/lake-superior-winter.jpg',
  'assets-src/raw/duluth-pier-light.jpg',
  'assets-src/raw/stpaul-skyline.jpg',
  'assets-src/raw/stpaul-night.jpg',
  'assets-src/raw/stpaul-cathedral.jpg',
  'assets-src/raw/north-woods-sunset.jpg',
  'assets-src/raw/bwca-portage.jpg',
  'assets-src/raw/street-rain.jpg',
  'assets-src/raw/street-lamp-snow.jpg',
  'assets-src/raw/candles.jpg',
  'assets-src/raw/bread.jpg',
  'assets-src/raw/cross-sky.jpg',
  'assets-src/raw/duluth-superior-st.jpg',
]

const missing = required.filter((p) => !fs.existsSync(path.join(root, p)))
if (missing.length) {
  console.error('Missing required source file(s):')
  for (const p of missing) console.error('  -', p)
  process.exit(1)
}
console.log('Required source files OK.')
