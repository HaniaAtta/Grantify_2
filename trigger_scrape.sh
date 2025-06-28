#!/bin/bash

read -p "Do you want to trigger scrape now? (y/n): " ans
if [[ "$ans" == "y" || "$ans" == "Y" ]]; then
  echo "[INFO] Triggering scrape via cron container..."
  docker exec grantly_cron curl -X POST http://fastapi:8000/api/scrape_all
else
  echo "[INFO] Scrape cancelled."
fi
