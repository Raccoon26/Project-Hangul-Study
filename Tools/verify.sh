#!/bin/sh
# Run from the project root. --portable explicitly omits native iOS verification.
set -eu
python3 Tools/check_monetization.py
python3 -m unittest discover -s Tools/ContentBuilder -v
if [ "${1:-}" = "--portable" ]; then
  printf '%s\n' 'Portable checks only. Xcode, SDK linking, iOS UI and StoreKit have NOT been tested.'
  exit 0
fi
if ! command -v xcodebuild >/dev/null 2>&1; then
  printf '%s\n' 'Native verification blocked: install/run Xcode on a Mac. Portable success is not a Release build.' >&2
  exit 2
fi
if [ -z "${TEST_DESTINATION:-}" ]; then
  printf '%s\n' 'Set TEST_DESTINATION to an installed iOS 17+ simulator (xcodebuild -showdestinations). Tests will not silently be skipped.' >&2
  exit 2
fi
xcodebuild -resolvePackageDependencies -project HangulStudy.xcodeproj -scheme HangulStudy
xcodebuild -project HangulStudy.xcodeproj -scheme HangulStudy \
  -configuration Debug -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' \
  CODE_SIGNING_ALLOWED=NO build
xcodebuild -project HangulStudy.xcodeproj -scheme HangulStudy \
  -configuration Release -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' \
  CODE_SIGNING_ALLOWED=NO build
# Also check device architecture; signing/distribution archive remains an owner release step.
xcodebuild -project HangulStudy.xcodeproj -scheme HangulStudy \
  -configuration Release -destination 'generic/platform=iOS' CODE_SIGNING_ALLOWED=NO build
xcodebuild -project HangulStudy.xcodeproj -scheme HangulStudy \
  -configuration Debug -destination "$TEST_DESTINATION" CODE_SIGNING_ALLOWED=NO test
