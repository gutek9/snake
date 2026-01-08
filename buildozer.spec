[app]

title = Terminal Snake
package.name = terminalsnake
package.domain = org.snake
source.dir = src
source.include_exts = py,png,jpg,kv
version = 0.1.0

android.sdk_path = /Users/madamek/.buildozer/android/platform/android-sdk
android.ndk_path = /Users/madamek/.buildozer/android/platform/android-ndk-r25b
android.sdkmanager_path = /Users/madamek/.buildozer/android/platform/android-sdk/cmdline-tools/latest/bin/sdkmanager
android.gradle_options = -Dorg.gradle.jvmargs=-Xmx6g

requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
