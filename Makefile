init:
	pdm install --prod

init-dev:
	pdm install

test:
	pdm run python ./sysadmin_telebot/main.py --log-level debug
