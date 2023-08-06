#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Fri Feb 17 12:54:13 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $
#

import sys

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import autologging

from autologging import logged, traced
from jinja2 import Template

from ecspylibs.initsetup import InitSetup


@traced
@logged
@dataclass
class InitCheck(InitSetup):
    """Initialize the environment using command line parameters and init file."""
    arguments: dict
    default_arguments: dict
    config: object = None,
    section: object = None

    def __post_init__(self):
        """Setup the InitCheck environment.  Setup default values then process the init file."""

        super().__post_init__()

        TOD = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        replace_tod = {
            "TOD": TOD,
        }

        if "--LOG" in self.arguments:
            self.log_file = Path(self.arguments['--LOG']).resolve(strict=False)
            try:
                self.log_file = self.log_file.resolve(strict=True)
            except FileNotFoundError as e:
                self.log_dir = self.log_file.parent.resolve(strict=False)
                try:
                    self.log_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
                    try:
                        self.log_file.touch(mode=0o644, exist_ok=True)
                    except PermissionError as e:
                        print(f"\nPermission Error: {e=}\n", file=sys.stderr)
                        sys.exit(1)
                    except Exception as e:
                        print(f"\nException: {e=}\n", file=sys.stderr)
                        sys.exit(1)
                except PermissionError as e:
                    print(f"\nPermission Error: {e=}\n", file=sys.stderr)
                    sys.exit(1)
                except Exception as e:
                    print(f"\nException: {e=}\n", file=sys.stderr)
                    sys.exit(1)
            except Exception as e:
                print(f"\nException: {e=}\n", file=sys.stderr)
                sys.exit(1)

            self.arguments['--LOG'] = self.log_file

        if "--output" in self.arguments:
            self.output_file = self.arguments['--output']
            self.output_file = Template(self.output_file).render(replace_tod)
            self.output_file = Path(self.output_file).resolve(strict=False)
            try:
                self.output_file = self.output_file.resolve(strict=True)
            except FileNotFoundError as e:
                self.output_dir = self.output_file.parent.resolve(strict=False)
                try:
                    self.output_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
                    try:
                        self.output_file.touch(mode=0o644, exist_ok=True)
                    except PermissionError as e:
                        print(f"\nPermission Error: {e=}\n", file=sys.stderr)
                        sys.exit(1)
                    except Exception as e:
                        print(f"\nException: {e=}\n", file=sys.stderr)
                        sys.exit(1)
                except PermissionError as e:
                    print(f"\nPermission Error: {e=}\n", file=sys.stderr)
                    sys.exit(1)
                except Exception as e:
                    print(f"\nException: {e=}\n", file=sys.stderr)
                    sys.exit(1)
            except Exception as e:
                print(f"\nException: {e=}\n", file=sys.stderr)
                sys.exit(1)

            self.arguments['--output'] = self.output_file

        if "--report" in self.arguments:
            self.report_file = self.arguments['--report']
            self.report_file = Template(self.report_file).render(replace_tod)
            self.report_file = Path(self.report_file).resolve(strict=False)
            try:
                self.report_file = self.report_file.resolve(strict=True)
            except FileNotFoundError as e:
                self.report_dir = self.report_file.parent.resolve(strict=False)
                try:
                    self.report_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
                    try:
                        self.report_file.touch(mode=0o644, exist_ok=True)
                    except PermissionError as e:
                        print(f"\nPermission Error: {e=}\n", file=sys.stderr)
                        sys.exit(1)
                    except Exception as e:
                        print(f"\nException: {e=}\n", file=sys.stderr)
                        sys.exit(1)
                except PermissionError as e:
                    print(f"\nPermission Error: {e=}\n", file=sys.stderr)
                    sys.exit(1)
                except Exception as e:
                    print(f"\nException: {e=}\n", file=sys.stderr)
                    sys.exit(1)
            except Exception as e:
                print(f"\nException: {e=}\n", file=sys.stderr)
                sys.exit(1)

            self.arguments['--report'] = self.report_file

        if "--pw" in self.arguments:
            self.passwd_file = Path(self.arguments['--pw']).resolve(strict=False)
            try:
                self.passwd_file = self.passwd_file.resolve(strict=True)
            except FileNotFoundError as e:
                self.passwd_dir = self.passwd_file.parent.resolve(strict=False)
                try:
                    self.passwd_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
                    try:
                        self.passwd_file.touch(mode=0o644, exist_ok=True)
                    except PermissionError as e:
                        print(f"\nPermission Error: {e=}\n", file=sys.stderr)
                        sys.exit(1)
                    except Exception as e:
                        print(f"\nException: {e=}\n", file=sys.stderr)
                        sys.exit(1)
                except PermissionError as e:
                    print(f"\nPermission Error: {e=}\n", file=sys.stderr)
                    sys.exit(1)
                except Exception as e:
                    print(f"\nException: {e=}\n", file=sys.stderr)
                    sys.exit(1)
            except Exception as e:
                print(f"\nException: {e=}\n", file=sys.stderr)
                sys.exit(1)

            self.arguments['--pw'] = self.passwd_file

        self.config_name = self.data['name']

        if 'admin' in self.data:
            self.admin_name = None
            self.admin_email = None
            self.admin_phone = None

            if 'name' in self.data['admin']:
                self.admin_name = self.data['admin']['name']

            if 'email' in self.data['admin']:
                self.admin_email = self.data['admin']['email']

            if 'phone' in self.data['admin']:
                self.admin_phone = self.data['admin']['phone']

        if 'email' in self.data:
            self.email_subject = None
            self.email_from = None
            self.email_to = None
            self.email_cc = None
            self.email_text_with_changes = None
            self.email_text_without_changes = None

            if 'subject' in self.data['email']:
                self.email_subject = self.data['email']['subject']

            name = email = None

            if 'from' in self.data['email']:
                if 'name' in self.data['email']['from']:
                    name = self.data['email']['from']['name']

                if 'email' in self.data['email']['from']:
                    email = self.data['email']['from']['email']

                self.email_from = f"{name} <{email}>"

            name = email = None

            if 'to' in self.data['email']:
                self.email_to = []
                for tmp in self.data['email']['to']:
                    if 'name' in tmp:
                        name = tmp['name']

                    if 'email' in tmp:
                        email = tmp['email']

                    self.email_to.append(f"{name} <{email}>")

            name = email = None

            if 'cc' in self.data['email']:
                self.email_cc = []
                for tmp in self.data['email']['cc']:
                    if 'name' in tmp:
                        name = tmp['name']

                    if 'email' in tmp:
                        email = tmp['email']

                    self.email_cc.append(f"{name} <{email}>")

            if 'text' in self.data['email']:
                if 'with_changes' in self.data['email']['text']:
                    self.email_text_with_changes = self.data['email']['text']['with_changes']

                if 'without_changes' in self.data['email']['text']:
                    self.email_text_without_changes = self.data['email']['text']['without_changes']
