[Unit]
Description=Collector Engine
After=network.target

[Service]
Environment="PATH=[BASE_PATH]/.virtualenvs/backup_collector/bin"
EnvironmentFile=[BASE_PATH]/[PROJECT_PATH]/backup_collector/backup_collector/services/backup_collector.env
WorkingDirectory=[BASE_PATH]/[PROJECT_PATH]/backup_collector
RestartSec=1
ExecStart=[BASE_PATH]/.virtualenvs/backup_collector/bin/backup_collector ${SETTINGS_FILE} ${DEBUG}
ExecStop=/bin/kill -WINCH ${MAINPID}
KillSignal=SIGCONT
Restart=always
StartLimitBurst=10

[Install]
WantedBy=multi-user.target
