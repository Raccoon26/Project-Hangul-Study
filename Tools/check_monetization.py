#!/usr/bin/env python3
"""Release configuration guard. Reads source xcconfig or a built app's Info.plist.
No network requests. Missing production IDs are a valid ads-disabled development state.
Use --require-ads before releasing with ads enabled.
"""
import argparse,json,plistlib,re
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
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--built-info',type=Path)
    parser.add_argument('--require-ads',action='store_true')
    args=parser.parse_args()
    if args.built_info:
        info=plistlib.loads(args.built_info.read_bytes())
        app=info.get('GADApplicationIdentifier','');unit=info.get('AdMobInterstitialIdentifier','')
    else:
        values={k:v.strip()for k,v in re.findall(r'^(ADMOB_\w+)\s*=([^\n]*)',(ROOT/'Config/Release.xcconfig').read_text(),re.M)}
        app=values.get('ADMOB_APP_ID','');unit=values.get('ADMOB_INTERSTITIAL_ID','')
    try: status=validate(app,unit,args.require_ads)
    except ValueError as error:parser.exit(1,str(error)+'\n')
    print(json.dumps({'release_ads':status,'product_id':'remove_ads'},ensure_ascii=False))
if __name__=='__main__':main()
