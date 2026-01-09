[app]

title = Codex Snake
package.name = codexsnake
package.domain = org.snake
source.dir = src
source.include_exts = py,png,jpg,kv
version = 0.1.0
android.gradle_options = -Dorg.gradle.jvmargs=-Xmx6g
# Optionally set this via env var:
#   export P4A_PYTHON_PATH="/path/to/python3.10"
p4a.python_path = ${P4A_PYTHON_PATH}

requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
