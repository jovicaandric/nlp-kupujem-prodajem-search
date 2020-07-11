#!/usr/bin/env sh

# Replace API_BASE_URL in compiled environment.prod.ts with provided value
# and start nginx afterwards.
find '/usr/share/nginx/html' -name '*.js' -exec sed -i -e 's,API_BASE_URL,'"$API_BASE_URL"',g' {} \;

nginx -g "daemon off;"
