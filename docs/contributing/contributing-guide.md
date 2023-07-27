Contributing to streamdeck_ui
========

Looking for a useful open source project to contribute to?
Want your contributions to be warmly welcomed and acknowledged?
Welcome! You have found the right place.

## Getting streamdeck_ui set up for local development
The first step when contributing to any project is getting it set up on your local machine. streamdeck_ui aims to make this as simple as possible.

Account Requirements:

- [A valid GitHub account](https://github.com/join)

Base System Requirements:

- Python3.8+
- poetry
- bash or a bash compatible shell (should be auto-installed on Linux / Mac)

Once you have verified that you system matches the base requirements you can start to get the project working by following these steps:

1. [Fork the project on GitHub](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/fork).
    * Make sure you untick the "copy the main branch only" option. This will ensure you have a full copy of the project to work with.
2. Clone your fork to your local file system:
    `git clone https://github.com/$GITHUB_ACCOUNT/streamdeck_ui.git`
3. `cd streamdeck_ui`
4. `poetry install`

## Making a contribution
Congrats! You're now ready to make a contribution! Use the following as a guide to help you reach a successful pull-request:

1. Check the [issues page](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/issues) or [discussions](https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/discussions) on GitHub to see if the task you want to complete is listed there.
    - If it's listed there, write a comment letting others know you are working on it.
    - If it's not listed in GitHub issues or discussions, go ahead and log a new issue. Then add a comment letting everyone know you have it under control.
        - If you're not sure if it's something that is good for the main streamdeck_ui project and want immediate feedback, you can discuss it on [Discord](https://discord.gg/ZCZesnEj4).
2. Create an issue branch for your local work `git checkout -b issue/$ISSUE-NUMBER origin/develop`.
3. Do your magic here.
4. Ensure your code matches the [HOPE-8 Coding Standard](https://github.com/hugapi/HOPE/blob/master/all/HOPE-8--Style-Guide-for-Hug-Code.md#hope-8----style-guide-for-hug-code) used by the project.
5. Submit a pull request to the main project repository via GitHub.
    * Make sure your target branch is set to `develop`.

Thanks for the contribution! It will quickly get reviewed, and, once accepted, will result in your name being added to the acknowledgments list :).

## Thank you!
I can not tell you how thankful we are for the hard work done by streamdeck-linux-gui contributors like *you*.

Thank you!

The streamdeck-linux-gui users! :heart:
