# Changelog

## [1.2.0a0] - 2023-03-30

### Added

- Attach glue42dash object to the global window object which includes lib version and glueInstance.

## [1.1.0a0] - 2023-02-14

### Added

- Add extra info to Channels and Context to indicate Interop updater instance.

## [1.0.0a3] - 2022-11-17

### Changed

- Updated Dash to version 2.
- Updated @glue42/react-hooks packages.

## [1.0.0a2] - 2022-11-16

### Changed

- Updated Glue42 component PropTypes.

## [1.0.0a1] - 2022-08-24

### Changed

- Updated components PropTypes.

## [1.0.0a0] - 2021-08-27

### Changed

- Breaking changes. See official documentation - https://docs.glue42.com/getting-started/how-to/glue42-enable-your-app/dash/index.html.

## [0.0.3] - 2020-08-20

### Changed

- Improved error handing in the `methodInvoke` and `methodRegister` components.
- The `definition` property type of `methodRegister` accepts either a string or an object.
- Added more reference comments to the component properties.

## [0.0.2] - 2020-07-31

### Added

- Leaving the current Channel.
- Joining a Channel.
- Getting the list of available Channels.

### Changed

- Raising notifications through the Glue42 Notifications API.

## [0.0.1] - 2020-07-29

### Added

- Invoking Interop methods.
- Registering Interop methods.
- Window opening.
- GNS notification raising.
- Glue42 Contexts - subscribing and updating a shared context.
- Glue42 Channels - subscribing to a Channel and publishing data to the current Channel.
