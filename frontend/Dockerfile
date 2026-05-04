# Static site (login, dashboard, etc.)
FROM nginx:1.27-alpine

COPY public/ /usr/share/nginx/html/

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=5 \
    CMD wget -qO- http://127.0.0.1/login.html > /dev/null || exit 1
