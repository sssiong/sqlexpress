# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.3] 2022-08-18
### Added
- Raise `YamlParsingFailed` exception if parsing of yaml file fails

### Changed
- Raise `QueryParsingFailed` exception instead of `InvalidStructure` exceptin when parsing of SQL file fails
- Make webserver an extra requirement that can only be installed using `pip install sqlexpress[web]`

## [0.2.2] 2022-08-16
### Added
- Raise `InvalidStructure` exception if parsing of SQL file fails

## [0.2.1] 2022-06-01
### Fixed
- Fix missing flask package & templates error

## [0.2.0] 2022-05-29
### Added
- Webserver with GUI to view relationships between source tables based on the parsed SQLs
- Allow environment variables in SQL to be substituted before parsing

## [0.1.0] 2022-05-03
### Added
- SQL parser to extract source tables
