# Sysadmin Telegram Bot

### Introduction
Because of some strange circumstances, I'm the de facto administrator for a Linux server in my workplace.

I got sick of having to ssh into the server and manually check the system's status, so I decided to make this bot. Off the clock though, because I enjoyed the idea and wanted to have a project of my own.

Now I can check on the server's status very quickly just by having this bot running on the server, prepared with well chosen informational commands that I can either trigger or have sent to me on an interval.


### How to set up
1. `cp ./sysadmin_telebot/COMMAND_TEMPLATE.yml ./sysadmin_telebot/local_config.yml`
    - Can also be any other name, so long as the formatting remains the same. Specify custom files with the `-c` argument.

2. In the format provided, add any shell commands into the `constants` section that you want to run on init or repeatedly on an interval.
    - every (int): How frequently, in seconds, to repeat the given command. If not provided, command is run at bot init and never again. Optional
    - prefix (str): Prepended to execute output. Optional
    - execute (str): Shell command that the bot will execute and send the result of to the user or chat specified in sendto. Required
    - suffix (str): appended to execute output. Optional
    - sendto (str, int): id of a user or chat to send the message to. Required

3. In the format provided, add any shell commands that you want users to be able to trigger into the `commands` section.
    - reactto (str): Name of command that the bot will react to in telegram. /reactto. Required
    - execute (str): Shell command that the bot will execute and send the result of to the user who triggered the command. Required

### How to run
1. `pipenv install && pipenv shell`
2. `cd sysadmin_telebot`
3. `python3 ./main.py`

Preferably, execute the bot inside of a screen or tmux session so that it can be hidden and re-captured by the executing user.


### Important notes
It is up to the person setting up the bot to create and use responsible commands. You can cause damage via the bot if you add dangerous commands to the bot's config.

For this reason, I have not created any ability to add commands to the bot after init, nor to provide commands to the bot via telegram messages.


### Known issues
If you provide an accessible command which has a long or indefinite runtime, the thread that command is executed in will stall, and that command will never complete. I'm fairly certain this does not cause the bot to stall across the board, but it will consume CPU time and memory in a form of memory leak. To my knowledge, this cannot be resolved; the user is responsible for providing non-destructive commands for the bot to be able to execute.

If you stop the bot in the middle of a command execution, the process that was being executed will be orphaned until its natural completion and destruction, or indefinitely. To my knowledge, this cannot be resolved.

### Future additions
* Create a "danger mode" option, which allows the user to execute any command via messaging the bot on telegram.
    - Activated via argv when starting the program
    - Triggers a blocking warning before the bot initializes, preventing the bot from starting until the user confirms their choice.

* Allow importing bash scripts instead of writing directly into config

* Add extensive debug logging



-----

### ETC.

Author: Gregory Danielson (@gregdan3)

Last updated: 11/06/2019
