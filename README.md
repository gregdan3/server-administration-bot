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

##### Configuring

```yml
---
owner: "[your Telegram ID]"

constants:
  init_example: # any name
    execute: "[command]"
    prefix: "This will appear on the line before your command output" # optional
    suffix: "This will appear on the line after your command output" # optional
    sendto:
      - "Any telegram user ID"
      - "Any number of these"
      - "Can also be a group ID if the bot is in the group"

  repeat_example: # any name
    every: [integer number of seconds]
    execute: "Command to run every number of seconds as specified"
    prefix: "This will appear on the line before your command output" # optional
    suffix: "This will appear on the line after your command output" # optional
    sendto:
      - "Any telegram user ID"
      - "Any number of these"
      - "Can also be a group ID if the bot is in the group"
    sleep: ""

commands:
  example: # any name
    reactto: "sysinfo" # command user inputs
    execute: "lshw" # command run in shell
```

### How to run

1. `pdm install`
2. `pdm run python ./sysadmin-telebot/main.py`

Preferably, execute the bot inside of a screen or tmux session so that it can be hidden and re-captured by the executing user.

### Convenient testing tool

You can go to `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates` to see all the recent messages your bot has sent and received, as well as group additions/removals and other interactions. This way,
if you lose access to your bot for some reason, you can still see what it's been doing, if it's still running.

### Important notes

It is up to the person setting up the bot to create and use responsible commands. You can cause damage via the bot if you add dangerous commands to the bot's config.

For this reason, I have not created any ability to add commands to the bot after init, nor to provide commands to the bot via telegram messages.

### Known issues

If you provide an accessible command which has a long or indefinite runtime, the thread that command is executed in will stall, and that command will never complete. I'm fairly certain this does not cause the bot to stall across the board, but it will consume CPU time and memory in a form of memory leak. To my knowledge, this cannot be resolved; the user is responsible for providing non-destructive commands for the bot to be able to execute.

If you stop the bot in the middle of a command execution, the process that was being executed will be orphaned until its natural completion and destruction, or indefinitely. To my knowledge, this cannot be resolved.

### Future additions

- Create a "danger mode" option, which allows the user to execute any command via messaging the bot on telegram.

  - Activated via argv when starting the program
  - Triggers a blocking warning before the bot initializes, preventing the bot from starting until the user confirms their choice.

- Allow importing bash scripts instead of writing directly into config

- Add extensive debug logging

- Allow scripts running on a time interval to "timeout" once they occur

  - For example: `dmesg | grep segfault` will only send a message if there is content in the command...
  - But you might not want to see the same message on every repeat, once you see it the first time!
  - So `timeout` will delay that command from executing again for a set period of time, likely by sleeping that thread.

- Allow scripts running on a time interval to execute at a specific time, as opposed
  to on a given interval set by bot start
  - If this could be cron-like, that would be awesome

### Annotated Config

TODO

```yml
constants: # All commands which are run at init or on specified intervals, without user input, REQUIRED KEY
  init: # no every argument means to execute once at beginning of runtime
    execute: "hostname --long" # execute will be run as a shell command, and the output returned
    prefix: "Hi! Waking up on host " # will be attached before command output
    suffix: "\nHave a nice day!" # will be attached after command output
    sendto: "1" # a user or chat to send to, which the bot has permissions for

  another: # you can have more than one of these
    execute: "ls -la" # can be any shell command, including piped programs.
    prefix: "Current dir files: \n" # any special character is legal, probably?
    sendto: "1"

  conntest: # the names of keys are irrelevant
    every: 60 # measured in seconds
    execute: "ping -c 1 google.com" # if a given command takes a long time, outside the interval,
    sendto: "1" # it will only re-execute once instead of queueing many executions

  sysdata: # key names can be used for your own purposes
    every: 40 #
    execute: "uname -r"
    sendto: "1"

commands: # all commands which can be triggered by users by the `reactto` command name, REQUIRED KEY
  info: # keynames here are still irrelevant
    reactto: "sysinfo" # reactto means the name of the command that must be executed to get the result
    execute: "lshw" # same as execute above, shell command to execute

  blocks:
    reactto: "blocks"
    execute: "lsblk"

  cpu:
    reactto: "processor"
    execute: "lscpu"
```
