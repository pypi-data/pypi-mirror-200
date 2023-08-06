The configuration is a JSON structure. We'll use the following for the
coming examples.

```JSON
{
  "courses": {
    "datintro22": {
      "timesheet": {
        "url": "https://sheets.google..."
      },
      "schedule": {
        "url": "https://timeedit.net/..."
      }
    }
  }
}
```

The format is actually irrelevant to anyone outside of this library,
since it will never be accessed directly anyway. But it will be used to
illustrate the examples.

We can access values by dot-separated addresses. For instance, we can
use `courses.datintro22.schedule.url` to access the TimeEdit URL of the
datintro22 course.

Let's have a look at some usage examples. Say we have the program
`nytid` that wants to use this config module and subcommand.

```python
import typer
import typerconf as config

cli = typer.Typer()
# add some other subcommands
config.add_config_cmd(cli)
```

We want the CLI command to have the following form when used with
`nytid`.

```bash
  nytid config courses.datintro22.schedule.url --set https://timeedit.net/...
```

will set the configuration value at the path, whereas

```bash
  nytid config courses.datintro22.schedule.url
```

will return it.

Internally, `nytid`'s different parts can access the config through the
following API.

```python
import typerconf as config

url = config.get("courses.datintro22.schedule.url")
```
