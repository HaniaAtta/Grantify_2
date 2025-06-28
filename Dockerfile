FROM python:3.12-slim


WORKDIR /app

COPY . .

# Install system packages including cron
RUN apt-get update && apt-get install -y \
    cron \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Add crontab file
COPY crontab /etc/cron.d/my-cron-job

# Give execution rights and install the cron job
RUN chmod 0644 /etc/cron.d/my-cron-job \
    && crontab /etc/cron.d/my-cron-job

# Create log file to view cron logs
RUN touch /var/log/cron.log

# Copy and make trigger script executable
COPY trigger_scrape.sh /trigger_scrape.sh
RUN chmod +x /trigger_scrape.sh


# Add start.sh script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run both cron and app
CMD ["/start.sh"]

