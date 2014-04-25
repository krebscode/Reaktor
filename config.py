from os.path import abspath, expanduser
import re

debug = True

name = 'crabmanner'

workdir = expanduser('~') + '/state'

irc_alarm_timeout = 300
irc_hammer_interval = 10
irc_kill_timeout = 360
irc_nickname = name
irc_server = 'irc.freenode.org'
irc_port = 6667
irc_restart_timeout = 5
irc_channels = [
  '#krebs'
]
admin_file='admin.lst'
auth_file='auth.lst'

config_filename = abspath(__file__)

# me is used, so name cannot kill our patterns below
me = '\\b' + re.escape(name) + '\\b'
me_or_us = '(?:' + me + '|\\*)'

def default_command(cmd, env={}):
  return {
    'capname': cmd,
    'pattern': '^' + me_or_us + ':\\s*' + cmd + '\\s*(?:\\s+(?P<args>.*))?$',
    'argv': [ 'commands/' + cmd ],
    'env': env
  }

public_commands = [
  default_command('caps', env={
    'config_filename': config_filename
  }),
  default_command('hello'),
  default_command('badcommand'),
  default_command('rev'),
  default_command('uptime'),
  default_command('nocommand'),
  {
    'capname': 'tell',
    'pattern': '^' + me_or_us + ':\\s*' + 'tell' + '\\s*(?:\\s+(?P<args>.*))?$',
    'argv': [ 'commands/tell-on_privmsg' ],
    'env': { 'state_file': workdir + '/tell.txt' }
  },
  # command not found
  { 'pattern': '^' + me_or_us + ':.*',
    'argv': [ 'commands/respond','You are made of stupid!'] },
  # "highlight"
  { 'pattern': '.*' + me + '.*',
    'argv': [ 'commands/say', 'I\'m famous' ] },
  # identify via direct connect
  { 'capname': 'identify',
    'pattern': '^identify' + '\\s*(?:\\s+(?P<args>.*))?$',
    'argv' : [ 'commands/identify' ]}
]
commands = [
  default_command('reload')
]

on_join = [
  {
    'capname': 'tell',
    'argv': [ 'commands/tell-on_join' ],
    'env': { 'state_file': workdir + '/tell.txt' }
  }
]
