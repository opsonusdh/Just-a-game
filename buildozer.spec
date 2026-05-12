[app]
title           = Just a game
package.name    = justagame
package.domain  = org.opsonusdh
version         = 1.0

source.dir      = .
source.include_exts = py,png,jpg


requirements = pygame2

p4a.branch = v2024.01.21

android.minapi  = 24
android.api     = 33
android.ndk     = 25c
android.archs   = arm64-v8a

p4a.bootstrap   = sdl2

orientation     = portrait
fullscreen      = 1

[buildozer]
log_level    = 2
warn_on_root = 1
