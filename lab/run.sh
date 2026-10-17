#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-jellyfin-playlist-itemids}"
export JELLYFIN_URL="${JELLYFIN_URL:-http://127.0.0.1:18800}"
export PYTHONUNBUFFERED=1
chmod +x poc.py

LABEL="JELLYFIN-PLAYLIST-ITEMIDS"
WITNESS="JELLYFIN-PLAYLIST-ITEMIDS-WITNESS"
IMAGE="jellyfin/jellyfin:12.2"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 jellyfin || true
  down
  exit 1
}

seed_media() {
  mkdir -p media/private-a media/public-b
  local private_mp4="media/private-a/${WITNESS}.mp4"
  local public_mp4="media/public-b/public-dummy.mp4"
  echo "== seed media =="
  if ! command -v ffmpeg >/dev/null 2>&1; then
    fail_setup "ffmpeg-missing"
  fi
  ffmpeg -y -hide_banner -loglevel error \
    -f lavfi -i "color=c=black:s=32x32:d=0.2" \
    -c:v mpeg4 -q:v 8 -pix_fmt yuv420p \
    -metadata title="${WITNESS}" \
    -metadata comment="${WITNESS}" \
    "${private_mp4}"
  ffmpeg -y -hide_banner -loglevel error \
    -f lavfi -i "color=c=blue:s=32x32:d=0.2" \
    -c:v mpeg4 -q:v 8 -pix_fmt yuv420p \
    "${public_mp4}"
  printf '%s' "${WITNESS}" >> "${private_mp4}"
  if [[ ! -s "${private_mp4}" ]] || [[ ! -s "${public_mp4}" ]]; then
    fail_setup "media-seed-empty"
  fi
  echo "IOC media-seed private=$(wc -c < "${private_mp4}" | tr -d ' ') public=$(wc -c < "${public_mp4}" | tr -d ' ')"
}

trap down EXIT

echo "== docker compose down (clean) =="
down
seed_media

if ! docker image inspect "${IMAGE}" >/dev/null 2>&1; then
  echo "== docker pull ${IMAGE} =="
  docker pull "${IMAGE}" || fail_setup "image-pull-failed"
fi

echo "== docker compose up =="
up_ok=0
for attempt in $(seq 1 8); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up -d; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 20
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait ${JELLYFIN_URL}/Startup/User =="
ready=0
for i in $(seq 1 90); do
  ping_code="$(curl -sS -o /tmp/jellyfin-playlist-itemids-ping.txt -w '%{http_code}' --max-time 8 \
    "${JELLYFIN_URL}/System/Ping" || true)"
  user_code="$(curl -sS -o /tmp/jellyfin-playlist-itemids-startup-user.txt -w '%{http_code}' --max-time 8 \
    "${JELLYFIN_URL}/Startup/User" || true)"
  if [[ "${user_code}" == "200" ]]; then
    ready=1
    echo "IOC jellyfin-ready attempt=${i} ping=${ping_code} startup-user=${user_code}"
    break
  fi
  echo "IOC jellyfin-wait attempt=${i} ping=${ping_code} startup-user=${user_code}"
  sleep 3
done
if [[ "${ready}" != 1 ]]; then
  fail_setup "jellyfin-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
