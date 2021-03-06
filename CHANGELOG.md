# Changelog
All notable changes to this project will be documented in this file.

## [0.0.6.2] - 2021-11-13
### Fixed
- Error in panel

## [0.0.6.1] - 2021-11-01
### Fixed
- Environment node uses "Environment" a very often, added this to check for old enviremont textures
- Correct default Saturation values in Node Group

## [0.0.6] - 2021-10-31
### Added
- auto-transfer old environment texture images > prevents from relinking them when switching modes

## [0.0.5] - 2021-10-30
### Changed
- World Control is now created in its own world named "WorldControl"

### Added
- Clean old setup when switching between advanced and basic
- WorldControl has its own world, so we dont mess with user own setup worlds. Easier for cleaning
- Easy switching operator, switch easy between basic and advanced

## [0.0.4] - 2021-10-30
### Changed
- Moved panel to View catergory
- Dynamic naming moved to panel itself > Panel Header has font size issue

## [0.0.3] - 2021-10-29
### Added
- Reset operator > set all inputs to default
- Panel view easy access from 3d viewport

## [0.0.2] - 2021-10-28
### Fixed 
- The Add function was visible in materials nodes as well, it added empty node in material, added poll to customnodecategrory 

### Changed
- Simplified node names on catergory, stripped "control"
- NodeGroup with was to narrow, added width

## [0.0.1] - 2021-10-27
### Added 
- Initial release repo 

## Notes
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
<!--### Official Rigify Info-->

[0.0.6.2]:https://github.com/schroef/World_Control/releases/tag/v0.0.6.2
[0.0.6.1]:https://github.com/schroef/World_Control/releases/tag/v0.0.6.1
[0.0.6]:https://github.com/schroef/World_Control/releases/tag/v0.0.6
[0.0.5]:https://github.com/schroef/World_Control/releases/tag/v0.0.5
[0.0.4]:https://github.com/schroef/World_Control/releases/tag/v0.0.4
[0.0.3]:https://github.com/schroef/World_Control/releases/tag/v0.0.3
[0.0.2]:https://github.com/schroef/World_Control/releases/tag/v0.0.2
[0.0.1]:https://github.com/schroef/World_Control/releases/tag/v0.0.1