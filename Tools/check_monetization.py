#!/usr/bin/env python3
"""Release configuration guard. Reads source xcconfig or a built app's Info.plist.
No network requests. Missing production IDs are a valid ads-disabled development state.
Use --require-ads before releasing with ads enabled.
"""
import argparse,json,plistlib,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEST_PUBLISHER='3940256099942544'
def validate(app,unit,require=False):
    if not app and not unit:
        if require:raise ValueError('Production AdMob IDs are absent; ads must remain disabled.')
        return 'disabled: production IDs absent'
    if TEST_PUBLISHER in app or TEST_PUBLISHER in unit:
        raise ValueError('Official Google TEST publisher found in Release configuration.')
    if not re.fullmatch(r'ca-app-pub-\d{16}~\d{10}',app):raise ValueError('Invalid production App ID.')
    if not re.fullmatch(r'ca-app-pub-\d{16}/\d{10}',unit):raise ValueError('Invalid production interstitial Ad Unit ID.')
    if app.split('~')[0] != unit.split('/')[0]:raise ValueError('App and ad unit must belong to the same publisher.')
    return 'configured: confirm account ownership and consent in AdMob before publishing'
def validate_release_settings(text,require=False):
    values={k:v.strip()for k,v in re.findall(r'^(ADMOB_\w+)\s*=([^\n]*)',text,re.M)}
    app=values.get('ADMOB_APP_ID','');unit=values.get('ADMOB_INTERSTITIAL_ID','')
    status=validate(app,unit,require)
    conditions=re.search(r'^SWIFT_ACTIVE_COMPILATION_CONDITIONS\s*=([^\n]*)',text,re.M)
    disabled=conditions is not None and 'HANGUL_ADS_DISABLED' in conditions.group(1)
    exclusions=re.search(r'^EXCLUDED_SOURCE_FILE_NAMES\s*=([^\n]*)',text,re.M)
    excluded=exclusions.group(1) if exclusions else ''
    if not app and not unit:
        if not disabled or not all(name in excluded for name in ('GoogleMobileAds*','UserMessagingPlatform*')):
            raise ValueError('Missing AdMob IDs require the ads-disabled compiler flag and both SDK link exclusions; a runtime guard cannot prevent the SDK startup crash.')
    elif disabled or any(name in excluded for name in ('GoogleMobileAds','UserMessagingPlatform')):
        raise ValueError('Production IDs configured but SDK remains excluded. Remove the ads-disabled compiler flag and SDK exclusions together, then rebuild and verify the signed app.')
    return status
def validate_built_app(info_path,require=False):
    info=plistlib.loads(info_path.read_bytes())
    app=info.get('GADApplicationIdentifier','');unit=info.get('AdMobInterstitialIdentifier','')
    status=validate(app,unit,require)
    executable=info_path.parent/info['CFBundleExecutable']
    linked=subprocess.check_output(['otool','-L',str(executable)],text=True)
    # Xcode can link these packages as dynamic frameworks or statically. ObjC
    # runtime class names survive stripping, unlike a regular symbol-table check.
    binary=executable.read_bytes()
    included=[name in linked or objc in binary for name,objc in (
        ('GoogleMobileAds',b'GADMobileAds\0'),('UserMessagingPlatform',b'UMPConsentInformation\0'))]
    if not app and not unit and any(included):
        raise ValueError('Ads-disabled app still loads an advertising SDK and can crash before launch.')
    if app and not all(included):
        raise ValueError('Configured advertising SDK is missing from the built executable.')
    return status
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--built-info',type=Path)
    parser.add_argument('--require-ads',action='store_true')
    args=parser.parse_args()
    try:
        status=validate_built_app(args.built_info,args.require_ads) if args.built_info else validate_release_settings((ROOT/'Config/Release.xcconfig').read_text(),args.require_ads)
    except ValueError as error:parser.exit(1,str(error)+'\n')
    print(json.dumps({'release_ads':status,'product_id':'remove_ads'},ensure_ascii=False))
if __name__=='__main__':main()
