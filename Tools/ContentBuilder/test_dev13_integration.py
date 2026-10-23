"""Executable config/real SQLite integration checks, NOT StoreKit/SDK/UI execution."""
import json,plistlib,re,sqlite3,tempfile,unittest
from pathlib import Path
from build_content import ROOT
from test_data05_content import query
from test_lookup_sql import user

class Dev13IntegrationTests(unittest.TestCase):
 def test_release_has_no_ad_ids_and_debug_uses_official_test_ids(self):
  release=(ROOT/'Config/Release.xcconfig').read_text()
  values=dict(re.findall(r'^(ADMOB_\w+)\s*=([^\n]*)',release,re.M))
  self.assertEqual(set(values),{'ADMOB_APP_ID','ADMOB_INTERSTITIAL_ID'})
  self.assertTrue(all(not v.strip() for v in values.values()))
  debug=(ROOT/'Config/Debug.xcconfig').read_text()
  self.assertIn('ca-app-pub-3940256099942544~1458002511',debug)
  self.assertIn('ca-app-pub-3940256099942544/4411468910',debug)
  for p in ROOT.rglob('*.swift'):
   if 'Tests' not in p.parts:self.assertNotRegex(p.read_text(),r'ca-app-pub-\d',str(p))
 def test_release_checker_rejects_test_ids_and_missing_required_ids(self):
  import importlib.util
  spec=importlib.util.spec_from_file_location('monetization_check',ROOT/'Tools/check_monetization.py')
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  self.assertTrue(module.validate('','').startswith('disabled'))
  with self.assertRaises(ValueError):module.validate('','',True)
  debug=(ROOT/'Config/Debug.xcconfig').read_text()
  values=dict(re.findall(r'^(ADMOB_\w+)\s*=([^\n]*)',debug,re.M))
  with self.assertRaises(ValueError):module.validate(values['ADMOB_APP_ID'].strip(),values['ADMOB_INTERSTITIAL_ID'].strip())
 def test_ads_disabled_release_excludes_sdk_before_its_load_time_initializer(self):
  import importlib.util
  from unittest.mock import patch
  spec=importlib.util.spec_from_file_location('monetization_startup_check',ROOT/'Tools/check_monetization.py')
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  release=(ROOT/'Config/Release.xcconfig').read_text()
  self.assertTrue(module.validate_release_settings(release).startswith('disabled'))
  for removed in ('HANGUL_ADS_DISABLED','GoogleMobileAds*','UserMessagingPlatform*'):
   with self.subTest(removed=removed),self.assertRaises(ValueError):module.validate_release_settings(release.replace(removed,''))
  with tempfile.TemporaryDirectory() as tmp:
   info=Path(tmp)/'Info.plist';info.write_bytes(plistlib.dumps({'CFBundleExecutable':'App','GADApplicationIdentifier':'','AdMobInterstitialIdentifier':''}))
   binary=Path(tmp)/'App';binary.write_bytes(b'local learning executable')
   with patch.object(module.subprocess,'check_output',return_value='App:\n /usr/lib/libsqlite3.dylib\n'):
    self.assertTrue(module.validate_built_app(info).startswith('disabled'))
   for sdk in ('GoogleMobileAds','UserMessagingPlatform'):
    with self.subTest(sdk=sdk),patch.object(module.subprocess,'check_output',return_value='App:\n @rpath/'+sdk+'.framework/'+sdk+'\n'),self.assertRaises(ValueError):module.validate_built_app(info)
   for objc in (b'GADMobileAds\0',b'UMPConsentInformation\0'):
    binary.write_bytes(objc)
    with self.subTest(static_sdk=objc),patch.object(module.subprocess,'check_output',return_value='App:\n /usr/lib/libsqlite3.dylib\n'),self.assertRaises(ValueError):module.validate_built_app(info)
 def test_info_uses_configuration_and_manifest_bundled(self):
  info=plistlib.loads((ROOT/'Resources/Info.plist').read_bytes())
  self.assertEqual(info['GADApplicationIdentifier'],'$(ADMOB_APP_ID)')
  self.assertEqual(info['AdMobInterstitialIdentifier'],'$(ADMOB_INTERSTITIAL_ID)')
  privacy=plistlib.loads((ROOT/'Resources/PrivacyInfo.xcprivacy').read_bytes())
  self.assertFalse(privacy['NSPrivacyTracking'])
  generator=(ROOT/'Tools/generate_project.py').read_text()
  self.assertIn('Resources/PrivacyInfo.xcprivacy',generator)
  self.assertIn('baseConfigurationReference',generator)
 def test_storekit_configuration_matches_nonconsumable_and_opt_in_scheme(self):
  data=json.loads((ROOT/'Config/RemoveAds.storekit').read_text())
  self.assertEqual(len(data['products']),1)
  product=data['products'][0]
  self.assertEqual(product['type'],'NonConsumable')
  self.assertEqual(product['productID'],'remove_ads')
  self.assertEqual(data['subscriptionGroups'],[])
  schemes=ROOT/'HangulStudy.xcodeproj/xcshareddata/xcschemes'
  self.assertNotIn('StoreKitConfigurationFileReference',(schemes/'HangulStudy.xcscheme').read_text())
  self.assertIn('StoreKitConfigurationFileReference',(schemes/'HangulStudy-StoreKit.xcscheme').read_text())
  view=(ROOT/'Views/RemoveAdsView.swift').read_text()
  self.assertIn('product.displayPrice',view);self.assertNotIn('¥800',view)
 def test_ads_are_after_committed_action_and_have_one_learning_callsite(self):
  views=[p for p in (ROOT/'Views').glob('*.swift') if 'ads.completed(' in p.read_text()]
  self.assertEqual([p.name for p in views],['VocabularyStudySessionView.swift'])
  code=views[0].read_text()
  self.assertLess(code.index('await model.act('),code.index('ads.completed('))
  self.assertIn('model.errorMessage == nil',code)
  self.assertIn('!before.completed',code)
  ads=(ROOT/'Services/AdService.swift').read_text()
  self.assertNotIn('SQLite',ads);self.assertNotIn('services.progress',ads)
  self.assertNotIn('Timer',ads)
  self.assertIn('requestGeneration == generation',ads)
 def test_no_learning_paywall_or_sdk_calls_in_learning_repositories(self):
  for folder in ['Repositories','LearningEngine','Persistence']:
   for path in (ROOT/folder).glob('*.swift'):
    self.assertNotIn('PurchaseService',path.read_text(),str(path))
    self.assertNotIn('GoogleMobileAds',path.read_text(),str(path))
 def test_continue_uses_latest_activity_and_2001_json_epoch(self):
  d=user(version=10);sql=query('SQLiteCurriculum','SELECT kind,target,level FROM')
  d.execute("INSERT INTO vocabulary_sets VALUES('set','intro',1,0,0)")
  d.execute("INSERT INTO vocabulary_sessions VALUES('v','set','{}',0,'active',2000000000)")
  d.execute("INSERT INTO listening_sessions VALUES('l','practice:intro:1',?,0)",[json.dumps({'updatedAt':2000000001-978307200})])
  self.assertEqual(d.execute(sql).fetchone()[0],'listening')
  d.execute("INSERT INTO production_sessions VALUES('p','lemma',?,0)",[json.dumps({'updatedAt':2000000002-978307200})])
  self.assertEqual(d.execute(sql).fetchone()[0],'production')
  d.execute("UPDATE production_sessions SET completed=1")
  self.assertEqual(d.execute(sql).fetchone()[0],'listening')
  d.execute("UPDATE listening_sessions SET completed=1")
  self.assertEqual(d.execute(sql).fetchone()[0],'vocabulary');d.close()
 def test_legacy_production_resume_uses_events_without_rewriting_progress(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'user.sqlite';d=user(path,10)
   d.execute("INSERT INTO production_sessions VALUES('p','lemma','{\"position\":3}',0)")
   d.execute("INSERT INTO grammar_sessions VALUES('g','grammar','{}',0,'active',10)")
   d.execute("INSERT INTO study_events VALUES('e','lemma',1,20,'day','UTC','production_polite','correct',0,'p',13)")
   d.execute("INSERT INTO srs_state VALUES('word','vocabulary','calendar_steps',1,'{\"stage\":4}',100,1,1)")
   d.commit();d.close();d=sqlite3.connect(path)
   self.assertEqual(d.execute(query('SQLiteCurriculum','SELECT kind,target,level FROM')).fetchone()[0],'production')
   self.assertEqual(d.execute('SELECT state_json FROM production_sessions').fetchone()[0],'{"position":3}')
   self.assertEqual(d.execute('SELECT state_json,due_at FROM srs_state').fetchone(),('{"stage":4}',100))
   self.assertEqual(d.execute('PRAGMA user_version').fetchone()[0],10);d.close()
if __name__=='__main__':unittest.main()
