#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from os.path import expanduser
from os import environ
import subprocess
import logging
import argparse
import re

# ---- Argument parser ----
def GetVersion() -> str:
    return "0.3.1"

def GetArgParser() -> argparse.ArgumentParser:
    tArgParser = argparse.ArgumentParser(usage="%(prog)s [OPTIONS]",
                                         description="List and connect to host entries from your ssh configuration")

    tArgParser.add_argument("-v", "--version", action="version", version = f"{tArgParser.prog} version {GetVersion()}")
    tArgParser.add_argument("-c", "--config", help="Path to configuration file", type=str, default=None, required=False)
    tArgParser.add_argument("-e", "--exclude", help="Exclude hosts based on python regular expression", type=str, default=None, required=False)
    tArgParser.add_argument("-s", "--ssh_command", help="SSH command", type=str, default="ssh", required=False)
    tArgParser.add_argument("-l", "--loop", help="Do not exit when ssh session ends, show host list again instead", action="store_true")
    tArgParser.add_argument("-t", "--terminal_tab_mode", help="Attempt to start ssh session in new tab/window of terminal", action="store_true")
    return tArgParser

# -- Logger setup ---
def setuplogging():
    # Set application wide debug level and format
    #logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',
                        level=logging.INFO)

# -- Read in entries from ssh config file ---
def CollectFromSSHConfig(Filename: str, RegExp: str, IgnoreCase: bool = False):
    try:
        with open(Filename, 'r') as f:
            Matches = re.findall(RegExp, f.read(), re.MULTILINE | (re.IGNORECASE if IgnoreCase else 0))
            #logging.debug (f'Searched {Filename} for {RegExp}. Result: {Matches}')
            return Matches
    except FileNotFoundError as e:
        logging.warning(f'File not found: {Filename}')
        return []
    except Exception as e:
        logging.debug(f'Skipping file {Filename}, cause: {str(e)}')
        return []

def ReadInHosts(InitialConfigfile: str):
    HostsRegExp = r'^\s*Host\s+(.+)'
    IncludesRegExp = r'^\s*Include\s+([\w:\/\_\-\"\.\\]+)\s*'

    # Check for includes
    SSHConfigs = []
    SSHConfigs.append(InitialConfigfile)
    IncludedConfigs = CollectFromSSHConfig(InitialConfigfile, IncludesRegExp, True)
    for i in IncludedConfigs: SSHConfigs.append(i)
    logging.debug(f'Searching SSH configuration files: {SSHConfigs}')

    # Read in Host entries from all found configuration files
    AllHosts = []
    for i in SSHConfigs:
        Hosts = CollectFromSSHConfig(i, HostsRegExp)
        for j in Hosts: AllHosts.append(j)
    logging.debug(f'Host list: {AllHosts}')

    return AllHosts

# -- List hosts and get choice from user ---
def PickChoice(Hosts):
    Message = str()
    for index, item in enumerate(Hosts):
        Message += f'{index + 1}) {item}\n'
    Message = Message.replace('"','') # Quotes not needed for display, looks a bit more clean

    try:
        # User may input more than one number, separated by whitespaces.
        # Thus: Split string, try to convert every substring into an integer and check
        # if it is a valid index value. Return a list of valid choices.
        Input = input(f'\n{Message}Connect to: ')
        Choices = Input.split()
        ChoicesChecked = []
        for i in Choices:
            try:
                if 0 < int(i) <= len(Hosts): ChoicesChecked.append(int(i) - 1)
            except ValueError: pass # Ignore ValueError - those entries will not be added to the ChoicesChecked list because the exception hits before the 'append' happens. No need to take further action here.
        return ChoicesChecked
    except KeyboardInterrupt:
        return []

# -- Get ssh config from users home directory if no path was supplied ---
def GetHomeSSHConfigPath():
    return expanduser('~/.ssh/config')

# -- Filter hosts --
def FilterHosts(Hosts, RegEx = None):
    try:
        if RegEx: FilteredHosts = [i for i in Hosts if not i == '*' and not re.fullmatch(RegEx, i)]
        else:     FilteredHosts = [i for i in Hosts if not i == '*']
    except re.error as e:
        logging.error(f'Invalid regular expression: {e.msg}')
        return None
    return FilteredHosts

# -- Get commandline to start new ssh connection --
def CommandLine(SSHCommand: str, Host:str, TerminalTabMode: bool = False):
    # Is it good style to hardcode this stuff here? Probably not. Do I care? Nope.
    Host_no_quotes = Host.replace('"','')
    if TerminalTabMode and ("WT_SESSION" in environ): return f'wt -w 0 new-tab {SSHCommand} {Host}'
    if TerminalTabMode and ("TMUX" in environ):       return f'tmux new-window -n "ssh {Host_no_quotes}" {SSHCommand} {Host}'
    return f'{SSHCommand} {Host}' # no TerminalTabMode or unsupported terminal

# --- main routine ----
def run_program():
    # setup logging
    setuplogging()

    # read in command line arguments
    parser = GetArgParser()
    targs = parser.parse_args()

    # Get host entries from configuration file
    SSHConfigFile = targs.config if targs.config is not None else GetHomeSSHConfigPath()
    logging.info(f'Reading host entries from {SSHConfigFile}')
    Hosts = ReadInHosts(SSHConfigFile)
    logging.debug(f'Hosts: {Hosts}')
    if len(Hosts) == 0:
        logging.info('No host entries found')
        return 0

    # Filter unwanted items
    FilteredHosts = FilterHosts(Hosts, targs.exclude)
    if not FilteredHosts:
        logging.info('No hosts, exit.')
        return 0

    # Let user choose a host and start ssh connection
    while True:
        Choice = PickChoice(FilteredHosts)
        if not Choice:  # Abort right away if list of choices is empty
            logging.info('Abort')
            return 0
        for i in Choice: # loop through list of chosen host indices, and run the ssh command for each one
            logging.info(f'Connecting to "{FilteredHosts[i]}"')
            try:
                Completed = subprocess.run(CommandLine(targs.ssh_command,
                                                       FilteredHosts[i],
                                                       targs.terminal_tab_mode),
                                           shell = True)
                logging.info(f'"{Completed.args}" returned "{Completed.returncode}"')
                if (not targs.loop) and (len(Choice) == 1): return Completed.returncode # When not in loop mode and only 1 choice was give: return exit code of the ssh session
            except KeyboardInterrupt:
                logging.info('Canceled by user')
                return 0
        if not targs.loop: return 0 # When in 'loop' mode: do not return, display list again and pick next choice

if __name__ == '__main__':
    sys.exit(run_program())
