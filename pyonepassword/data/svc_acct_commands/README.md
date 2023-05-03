# Service Account Command Directory


## Summary
The purpose of this directory is to enable validating 'op' commands, subcommands, and any options & arguments for compatibility with service accounts.


## Details
Each file in this folder is a JSON directory of top-level 'op' commands. For example, 'item', 'vault', 'group', etc. See `op --help` for a listing of 'op' commands.

Each JSON directory contains entries for subcommands compatible with service accounts. Each subcommand entry includes requirements & restrictions, if applicable, and other details required to parse the command to determine service account suitability. For example, the 'item get' subcommand requires a '--vault' argument with service accounts. The 'vault list' subcommand prohibits the '--user' option with service accounts.

## Example

Here is a JSON directory of the 'item' command's subcommands that are compatible with service accounts. Note that some subcommands require a "--vault" argument and some do not. Also note that some subcommands have a positional argument, and some do not.

```JSON
{
  "meta": {
    "version": 1,
    "command_name": "item"
  },
  "subcommands":{
    "get": {
      "has_arg": true,
      "required_options": ["--vault"],
      "prohibited_options": []
    },
    "template": {
      "list": {
        "has_arg": false,
        "required_options": [],
        "prohibited_options": []
      }
    },
    "list": {
      "has_arg": false,
      "required_options": [],
      "prohibited_options": []
    },
    "create": {
      "has_arg": false,
      "required_options": ["--vault"],
      "prohibited_options": []
    },
    "delete": {
      "has_arg": true,
      "required_options": ["--vault"],
      "prohibited_options": []
    }
  }
}

```
