# Changelog

All notable changes to the unraid-api project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2023-07-15

### First Stable Release
This is the first stable release of the unraid-api library, with full support for the current Unraid GraphQL API features.

### Breaking Changes
- Removed username/password authentication as it's no longer supported by the Unraid GraphQL API
- API key authentication is now required for all API calls

### Added
- Support for retrieving array devices with filesystem types (xfs, btrfs, vfat, zfs)
- Support for retrieving pool devices with filesystem types
- Support for retrieving boot device information
- Support for retrieving disk temperatures
- Support for retrieving SMART status
- Support for retrieving disk spindown settings
- Added `get_disk_smart` method to retrieve SMART data for a disk
- Added `get_spindown_delay` method to retrieve the spindown delay setting
- Added detailed exception documentation in the developer guide
- Added Home Assistant integration examples for disk temperature and SMART status sensors

### Changed
- Updated the CLI to display disk temperatures
- Updated the CLI to display SMART status
- Updated the CLI to display spindown settings
- Improved error handling and resilience
- Updated documentation to reflect API key authentication
- Added examples for new features in the developer guide

### Fixed
- Fixed issues with the CLI client when retrieving array information
- Fixed issues with the CLI client when retrieving system information
- Made the library more resilient to missing fields in the API response

## [0.1.3] - 2023-06-01

### Added
- Initial alpha release of the unraid-api library
- Support for array operations (start, stop, get status)
- Support for disk operations (mount, unmount, get info)
- Support for VM operations (start, stop, get info)
- Support for Docker operations (start, stop, get info)
- Support for system information retrieval
- CLI client for interacting with the API
