#!/usr/bin/env bash
# +12 Monkeys — Production Deploy Script
# Deploys backend stack (MongoDB + NANDA + Backend) and wires Vercel frontend.
#
# Usage:
#   ./deploy.sh railway   # Deploy backend to Railway, set Vercel env var
#   ./deploy.sh compose   # Deploy via docker-compose on current host
#   ./deploy.sh vercel    # (Re)deploy frontend to Vercel only
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

info()  { echo -e "${CYAN}▸${NC} $*"; }
ok()    { echo -e "${GREEN}✔${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC} $*"; }
err()   { echo -e "${RED}✖${NC} $*" >&2; }
need()  { command -v "$1" &>/dev/null || { err "$1 is required but not installed."; exit 1; }; }

# ─── Vercel frontend deploy ───────────────────────────────────────────────────
deploy_vercel() {
  need vercel
  info "Deploying frontend to Vercel…"
  cd "$SCRIPT_DIR/frontend"

  if [ -n "${BACKEND_URL:-}" ]; then
    info "Setting NEXT_PUBLIC_API_URL=$BACKEND_URL on Vercel project…"
    vercel env rm NEXT_PUBLIC_API_URL production --yes 2>/dev/null || true
    echo "$BACKEND_URL" | vercel env add NEXT_PUBLIC_API_URL production
    ok "Environment variable set."
  fi

  vercel deploy --prod --yes
  ok "Frontend deployed to Vercel."
}

# ─── Docker Compose (self-hosted) ────────────────────────────────────────────
deploy_compose() {
  need docker
  cd "$SCRIPT_DIR"

  ENV_FILE=".env.production"
  if [ ! -f "$ENV_FILE" ]; then
    err "Missing $ENV_FILE — copy .env.production.example and fill in values."
    exit 1
  fi

  info "Building and starting services with docker-compose…"
  docker compose -f docker-compose.prod.yml --env-file "$ENV_FILE" up -d --build

  info "Waiting for backend health check…"
  for i in $(seq 1 30); do
    if curl -sf http://localhost:${BACKEND_PORT:-8000}/health >/dev/null 2>&1; then
      ok "Backend is healthy."
      break
    fi
    [ "$i" -eq 30 ] && { err "Backend did not become healthy in 30s."; exit 1; }
    sleep 1
  done

  BACKEND_URL="http://$(hostname -f 2>/dev/null || echo localhost):${BACKEND_PORT:-8000}"
  ok "Backend stack running at $BACKEND_URL"
  echo ""
  warn "Set this in Vercel dashboard (or re-run with 'vercel' target):"
  echo "  NEXT_PUBLIC_API_URL=$BACKEND_URL"
}

# ─── Railway (cloud) ─────────────────────────────────────────────────────────
deploy_railway() {
  need railway
  cd "$SCRIPT_DIR"

  ENV_FILE=".env.production"
  if [ ! -f "$ENV_FILE" ]; then
    err "Missing $ENV_FILE — copy .env.production.example and fill in values."
    exit 1
  fi
  # shellcheck disable=SC1090
  source "$ENV_FILE"

  info "Linking Railway project (create one at https://railway.app if needed)…"
  railway link || { err "Run 'railway login' first, then 'railway link' to select your project."; exit 1; }

  # --- MongoDB ---
  info "Provisioning MongoDB plugin…"
  railway add --plugin mongodb 2>/dev/null && ok "MongoDB plugin added." || warn "MongoDB plugin may already exist."

  # --- NANDA Index ---
  info "Deploying NANDA Index service…"
  railway service create nanda 2>/dev/null || warn "nanda service may already exist."
  railway service set nanda
  railway variables set PORT=6900 ENABLE_FEDERATION="${ENABLE_FEDERATION:-false}"
  # MONGODB_URI is auto-injected by the plugin via Railway's reference variables
  railway variables set MONGODB_URI='${{MongoDB.MONGO_URL}}' MONGODB_DB="${MONGODB_DB:-twelve_monkeys}"
  railway up --service nanda --detach -d ./nanda-index
  ok "NANDA Index deploying…"

  # --- Backend ---
  info "Deploying Backend service…"
  railway service create backend 2>/dev/null || warn "backend service may already exist."
  railway service set backend
  railway variables set \
    ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
    NANDA_URL='${{nanda.RAILWAY_PRIVATE_DOMAIN}}:6900' \
    CORS_ORIGINS="${CORS_ORIGINS:-https://plus12monkeys.vercel.app}" \
    DEBUG=false \
    LLM_MODEL="${LLM_MODEL:-claude-sonnet-4-20250514}" \
    SESSION_TTL_MINUTES="${SESSION_TTL_MINUTES:-1440}" \
    SESSION_MAX_COUNT="${SESSION_MAX_COUNT:-500}"
  railway up --service backend --detach -d ./backend
  ok "Backend deploying…"

  # --- Get public URL ---
  info "Fetching backend public URL (may take a moment)…"
  sleep 5
  BACKEND_URL=$(railway service info backend --json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('serviceUrl',''))" 2>/dev/null || echo "")

  if [ -z "$BACKEND_URL" ]; then
    warn "Could not auto-detect backend URL."
    warn "Check Railway dashboard for the backend's public domain, then run:"
    echo "  BACKEND_URL=https://<your-backend>.up.railway.app ./deploy.sh vercel"
  else
    BACKEND_URL="https://$BACKEND_URL"
    ok "Backend URL: $BACKEND_URL"
    echo ""
    read -rp "Deploy frontend to Vercel with this backend URL? [Y/n] " yn
    case "${yn:-Y}" in
      [Nn]*) warn "Skipped. Set NEXT_PUBLIC_API_URL=$BACKEND_URL in Vercel manually." ;;
      *)     export BACKEND_URL; deploy_vercel ;;
    esac
  fi
}

# ─── Main ─────────────────────────────────────────────────────────────────────
case "${1:-}" in
  railway) deploy_railway ;;
  compose) deploy_compose ;;
  vercel)  deploy_vercel  ;;
  *)
    echo "Usage: $0 {railway|compose|vercel}"
    echo ""
    echo "  railway  — Deploy backend stack to Railway + wire Vercel frontend"
    echo "  compose  — Deploy backend stack via docker-compose on current host"
    echo "  vercel   — (Re)deploy frontend to Vercel only"
    echo ""
    echo "Prerequisites:"
    echo "  railway  → npm i -g @railway/cli && railway login"
    echo "  compose  → docker + docker compose"
    echo "  vercel   → npm i -g vercel && vercel login"
    exit 1
    ;;
esac
