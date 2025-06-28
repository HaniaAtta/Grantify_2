#!/bin/bash
cron
touch /var/log/cron.log
tail -f /var/log/cron.log &

# ✅ updated line here
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
