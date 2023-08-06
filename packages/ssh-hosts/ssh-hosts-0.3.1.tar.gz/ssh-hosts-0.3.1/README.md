# SSH-Hosts

Simple script to list all host entries in your SSH configuration. You can then choose to quickly connect to one of them.

## Installation

  * Install from pypi: ```pip install ssh-hosts```

  OR

  * Download the pip package from GitLab
  * Install it with pip, e.g. pip install sshhosts-0.3.1-py3-none-any.whl

## Usage

### Basic usage

Just run
```
ssh-hosts
```
Running with no arguments will read in your ssh configuration from ```~/.ssh/config``` and list all found host entries. Type the number of an entry to connect to that given host.

### Path to SSH configuration

```
ssh-hosts -c '<path to ssh config>'
```
This will read in the SSH configuration file from the given path instead of ```~/.ssh/config```.


### Excluding hosts

```
ssh-hosts -e '<python regex>'
```
You can exclude host entries from the list based on a Python regular expression which needs to match *exactly*.

e.g.
```
ssh-hosts -e 'foo'
```
Will only exclude a host named 'foo', but not one named 'foo1'. To exclude both 'foo' and 'foo1' you could use

```
ssh-hosts -e 'foo\w*'
```

...or any other appropriate Python regular expression.

### Using a custom ssh command

```
ssh-hosts -s '<shell/ssh command>'
```

You can supply a custom command which ssh-hosts will use when you pick a host. The default is just 'ssh'.

Examples:

Start ssh connection with debug output
```
ssh-hosts -s 'ssh -v'
```

### Terminal tab mode

Experimental.

Tries so start ssh connections in new tabs if running in *Windows Terminal*, or in new windows when running in *tmux*.

```
ssh-hosts --terminal_tab_mode
```

## Command line arguments overview

```
optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CONFIG, --config CONFIG
                        Path to configuration file
  -e EXCLUDE, --exclude EXCLUDE
                        Exclude hosts based on python regular expression
  -s SSH_COMMAND, --ssh_command SSH_COMMAND
                        SSH command
  -l, --loop            Do not exit when ssh session ends, show host list again instead
  -t, --terminal_tab_mode
                        Attempt to start ssh session in new tab/window of terminal
```
## Examples



## Licensing

Licensed under the MIT license, see also LICENSE.txt
