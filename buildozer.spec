[app]

title = Codex Snake
package.name = codexsnake
package.domain = org.snake
source.dir = src
source.include_exts = py,png,jpg,kv
version = 0.1.0
android.gradle_options = -Dorg.gradle.jvmargs=-Xmx6g
#
# Use a Python version compatible with pyjnius/Cython during builds.
# Adjust this path if you install a different pyenv version.
p4a.python_path = /Users/madamek/.pyenv/versions/3.10.14/bin/python

requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
