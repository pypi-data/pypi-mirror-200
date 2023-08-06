# Treecker

> What does it mean?

The name "Treecker" comes from the contraction of "tree" and "tracker".

> What is it for?

Treecker is a Python package to control the integrity of a directory.

> Is it hard to use?

Just type one of the available commands in a terminal.

## Background

Have you ever wondered if you had accidentally destroyed or altered a part of the data contained in your favorite directory without realizing it?
Do you want to be able to stamp a part of your data and to control at any time that they are still in the state where you had left them?
Do you think that one of your files has been corrupted, but you don't know which one?
If so, this package is for you.

## Features

This Python package is for inspecting and tracking the organization of files in a directory.
A snapshot of the tree structure is saved in a file placed at the root of the tracked directory.
At any time it is possible to compare the current state of the directory with the latest snapshot, and to save the new state.
The program can also check that the file and folder names match a regular expression.
This allows to detect errors in the naming of files.
These features are accessible via the following commands:

* `init`: To create the first snapshot of a directory.
* `status`: To display the changes since last snapshot.
* `commit`: To save the change in a new snapshot.
* `issues`: To display incorrectly named files and directories.

## Installation

You can find how to install the package in the [installation section](https://dustils.gitlab.io/treecker/practice/installation/index.html) of the documentation.

## Usage

You can find how to use the package in the [examples section](https://dustils.gitlab.io/treecker/practice/examples/index.html) of the documentation.

## Credits

* Dunstan Becht

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
