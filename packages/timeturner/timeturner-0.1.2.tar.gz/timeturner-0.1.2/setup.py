# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timeturner', 'timeturner.tools']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.10.5,<2.0.0',
 'rich>=13.3.1,<14.0.0',
 'tomlkit>=0.11.6,<0.12.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['timeturner = timeturner.run:entrypoint',
                     'tt = timeturner.run:entrypoint']}

setup_kwargs = {
    'name': 'timeturner',
    'version': '0.1.2',
    'description': '',
    'long_description': 'Time Turner\n===========\n\n## A Minimalistic Time Tracker.\n\nThis is a minimalistic time tracker that allows you to record when you start working, even if it is in the past, stop running activities now, and add activities from the past. It also ensures legal rest periods are included if you forgot to track them.\n\nIn the Harry Potter series, the Time-Turner is a magical device that allows the user to travel back in time. Time Turner is a time tracker that lets you "turn back time" and record activities from the past.\n\n**Warning, this is still an alpha release, the API is not stable yet.**\n\n## Usage\n\n### Starting an Activity\n\nTo start tracking an activity, run the following command:\n\n\n![`timeturner add`](img/add.svg)\n\nThis will record the current time as the start of your activity.\n\nIf you forgot to start tracking an activity yesterday, you can provide the start time with an additional parameter, `-10m` would mean 10 minutest ago. The full list of possible time values can be [seen further down](#examples-for-times)\n\n### Stopping an Activity\n\nTo stop tracking the current activity, run the following command:\n\n\n![`timeturner end`](img/end.svg)\n\n\nThis will record the current time as the end of your activity and calculate the total duration.\n\n### Adding a Past Activity\n\nIf you forgot to track an activity in the past, you can add it with `timeturner add <start_time> - <end_time>`\n\n![`timeturner add -- -1d@9:00 - +8h45m`](img/add_past.svg)\n\n## Configuration\n\n| Environment Variable       | Default Value                    | Description                                  |\n| -------------------------- | -------------------------------- | -------------------------------------------- |\n| TIMETURNER_CONFIG_HOME     | ~/$XDG_CONFIG_HOME/timeturner    | The directory for configuration files.       |\n| TIMETURNER_CONFIG_FILE     | timeturner.toml                  | The configuration file to use.               |\n| TIMETURNER_DATABASE__HOME  | value of $TIMETURNER_CONFIG_HOME | The directory to store the database file in. |\n| TIMETURNER_DATABASE__FILE  | timeturner.db                    | The database file to use.                    |\n| TIMETURNER_DATABASE__TABLE | pensive                          | The table to use in the database.            |\n\n## Examples\n\n### Examples for times\n\n<start_time> or <end_time> could be one of the following Examples:\n\n| Example         | Description                               |\n| --------------- | ----------------------------------------- |\n|                 | now                                       |\n| 9:00            | 9:00 today                                |\n| -1m             | 1 minute ago                              |\n| -1h             | 1 hour ago                                |\n| -1d             | 1 day ago, you will be asked for the time |\n| -1d@9:00        | 1 day ago 9:00                            |\n| +1m             | 1 minute from now                         |\n| +1h             | 1 hour from now                           |\n| 12 7:00         | 7:00 on the 12th of the current month     |\n| 02-28 9:00      | 9:00 on February 28 of the current year   |\n| 2022-02-28 9:00 | 9:00 on February 28, 2022                 |\n\n\n\n### Automatic Rest Periods\n\nIf you forget to track a rest period, the time tracker will reduce the required rest period before showing it. For periods greater than 4h 15 are reducted, for periods greater than 6:15 additional 30m are reducted.\n\n\n\nTODOs:\n- [ ] Add Changelog\n- [ ] Add Configuration\n  - [ ] ignore seconds\n  - [ ] freeze time, to generate useful images\n  - [ ] automatic rest periods\n- [ ] show and generate tui output\n- [ ] Add section about contributions\n- [ ] Add precommit hook to ensure code is formatted\n- [ ] Add version and git hash to build, so it can be shown in the tui\n- [ ] Generate docstrings for DB methods\n- [ ] Remove import command (it contains assumptions that will not be true for everyone)\n  - [ ] Document how to import data from other time trackers\n  - [ ] Add mode to convert hamster output to jsonl file.\n  - [ ] Add mode to import jsonl file\n- [ ] Add logging\n  - [ ] allow different log levels for database and application\n- [ ] add a change log\n- [ ] README\n  - [ ] auto generate config options\n- [ ] db\n  - [ ] add table for tags\n\n\nTODOS by command:\n\n- [ ] add\n  - [ ] allow passive activities\n  - [ ] allow sick days\n- [ ] end\n  - [ ] add tests\n\n- [ ] configure\n  - [ ] modify and write configfile\n  - [ ] allow to add aliases for commands\n    - [ ] e.g. new new add alias with setting passive to true\n- [ ] list\n  - [ ] split up multiday activities\n  - [ ] add option to show only open activities\n  - [ ] group by year, month, week, day\n  - [ ] add tests\n\n- [ ] undo (revert the last change)\n### Design Goals\n\n- minimalistic, little to type\n- enforce as little as possible\n- be clear\n- be extensible\n  - TODO: support plugins (maybe a later version)\n  - be able to use it programmatically\n  - be able to use it as a library\n\n\n### Open Questions\n\n- [ ] should the get_latest_segment return segments from the future (start_time in the future)?\n\n### Nice to have:\n- [ ] Build a minimal Docker image (maybe)\n- [ ] https://github.com/ines/termynal\n',
    'author': 'Olaf Gladis',
    'author_email': 'olaf@gladis.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
