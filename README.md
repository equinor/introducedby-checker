# IntroducedBy Checker Action 🔍

## How it works
When adding this action to a workflow it will scan all NuGet package references in the source code. The action will find and delete all package references marked with the `IntroducedBy` attribute. When this is done it creates a pull request with the changes.

## Why
Often times a package used directly will be dependent on a vulnerable package which introduces a transitive vulnerability. 
To mitigate this the a healthy version of the transitive dependency can be installed directly into the project.
Marking these dependencies with the `IntroducedBy` attribute makes them easier to manage. 

This action generates a pull request to remove the identified dependencies, allowing the `Snyk action` to scan the pull request and provide a 
report on which dependencies can be safely deleted and which ones need to be retained.

## Usage
Add the following to your workflow

``` yml
name: 🔍 IntroducedBy Checker 🔍
on:
  schedule:
    - cron: '0 0 * * 1'
jobs: 
  compliance_test:
    runs-on: ubuntu-latest
    name: IntroducedBy Checker
    permissions:
       pull-requests: write
       contents: write
    steps:
      - name: Checkout # Makes the source code available to be scanned
        id:   checkout
        uses: actions/checkout@v4 
      - name: Delete marked package references # Scans the source code for marked package references and deletes them
        id:   scan
        uses: equinor/introducedby-checker@v0.0.1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## The Team
[Info about our team.](https://github.com/equinor/team-semantic-infrastructure)

## Contributing
Please follow these steps to contribute:

Fork the repository on GitHub. Clone your fork and create a new branch for your feature or bugfix. Commit your changes to the new branch. Push your changes to your fork. Open a pull request from your fork to the original repository. Please ensure that your code follows the existing style and structure, and add tests where necessary.
