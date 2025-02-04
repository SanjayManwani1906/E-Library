cmd.exe /c start wsl.exe -e ~/go/bin/MailHog
cmd.exe /c start wsl.exe -e redis-server
cmd.exe /c start wsl.exe -e celery -A main.celery worker -l info
cmd.exe /c start wsl.exe -e celery -A main.celery beat -l info
cmd.exe /c start wsl.exe -e python3 main.py
cd frontend && npm run dev