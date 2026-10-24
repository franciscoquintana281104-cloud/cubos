#!/bin/zsh
# Publica los cambios de Cubos en GitHub Pages.
# Sube el número de caché del service worker para que los móviles
# que ya la tienen instalada reciban la versión nueva.
# Uso: ./actualizar.sh "qué ha cambiado"
set -e
cd "$(dirname "$0")"

actual=$(grep -o 'cubos-v[0-9]*' sw.js | grep -o '[0-9]*$')
nueva=$((actual + 1))
sed -i '' "s/cubos-v$actual/cubos-v$nueva/" sw.js

git add -A
git commit -m "${1:-Actualiza Cubos}"
git push
echo "Publicada la versión $nueva. En un par de minutos estará en el móvil."
