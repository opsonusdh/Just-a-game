[app]
title           = Just a game
package.name    = justagame
package.domain  = org.opsonusdh
version         = 1.0

source.dir      = .
source.include_exts = py,png,jpg

requirements = python3, pygame

android.minapi  = 24
android.api     = 33
android.ndk     = 25c
android.archs   = arm64-v8a

orientation     = portrait
fullscreen      = 1

[buildozer]
log_level  = 2
warn_on_root = 1
