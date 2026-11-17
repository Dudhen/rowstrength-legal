# Build AAB from the existing mobile Flutter project; never changes any source file.
$ErrorActionPreference='Stop'
if(-not (Test-Path '.\pubspec.yaml')){throw 'Run this in the Flutter project root (with pubspec.yaml).'}
if(-not (Test-Path '.\.env')){throw '.env is missing; do not publish without the correct configuration.'}
Write-Host 'Check that lib/main.dart is the MOBILE version, not main_windows.dart.' -ForegroundColor Yellow
Write-Host 'Check pubspec.yaml version: build number after + must exceed the current Play release.' -ForegroundColor Yellow
& flutter pub get
if($LASTEXITCODE -ne 0){throw 'flutter pub get failed'}
& flutter analyze
if($LASTEXITCODE -ne 0){throw 'flutter analyze failed; fix reported diagnostics first'}
& flutter build appbundle --release --dart-define-from-file=.env
if($LASTEXITCODE -ne 0){throw 'Flutter release build failed'}
$out='build\app\outputs\bundle\release\app-release.aab'
if(-not (Test-Path $out)){throw "AAB missing at $out"}
Write-Host "DONE: $((Resolve-Path $out).Path)" -ForegroundColor Green
