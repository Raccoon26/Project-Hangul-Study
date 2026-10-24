#!/usr/bin/env python3
"""Deterministic .xcodeproj writer. No external dependencies; run after adding files."""
import hashlib, json, plistlib, re
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
objects={}
def ident(name): return hashlib.sha256(name.encode()).hexdigest()[:24].upper()
def add(object_key,**fields):
    key=ident(object_key); objects[key]=fields; return key

def encode(value,level=0):
    if isinstance(value,dict):
        return '{\n'+''.join('\t'*(level+1)+json.dumps(k)+' = '+encode(v,level+1)+';\n' for k,v in value.items())+'\t'*level+'}'
    if isinstance(value,list): return '(\n'+''.join('\t'*(level+1)+encode(v,level+1)+',\n' for v in value)+'\t'*level+')'
    return json.dumps(str(value),ensure_ascii=False)

app_files=sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*.swift') if not {'Tests','.build','DerivedData'}.intersection(p.relative_to(ROOT).parts))
test_files=sorted(p.relative_to(ROOT).as_posix() for p in (ROOT/'Tests').glob('*.swift'))
ui_files=sorted(p.relative_to(ROOT).as_posix() for p in (ROOT/'Tests/UI').glob('*.swift'))
resources=['Resources/PrivacyInfo.xcprivacy','Resources/user-schema-v1.sql','Resources/user-migration-v2.sql','Resources/user-migration-v3.sql','Resources/user-migration-v4.sql','Resources/user-migration-v5.sql','Resources/user-migration-v6.sql','Resources/user-migration-v7.sql','Resources/user-migration-v8.sql','Resources/user-migration-v9.sql','Resources/user-migration-v10.sql','Resources/ja.lproj/Localizable.strings']
# Optional verified recordings keep their Audio/ folder in the app bundle.
if (ROOT/'Content/Audio').is_dir(): resources.append('Content/Audio')
test_resource_files=['Resources/content-fixture.sqlite','Config/RemoveAds.storekit','Content/data06-ids.json']
ui_resource_files=['Resources/content.sqlite']
configuration_files=['Config/Debug.xcconfig','Config/Release.xcconfig']
refs={}
for file in app_files+test_files+ui_files+resources+test_resource_files+ui_resource_files+configuration_files:
    filetype='folder' if (ROOT/file).is_dir() else 'sourcecode.swift' if file.endswith('.swift') else 'text.plist.strings' if file.endswith('.strings') else 'text.xcconfig' if file.endswith('.xcconfig') else 'text'
    refs[file]=add('file:'+file,isa='PBXFileReference',lastKnownFileType=filetype,path=file,sourceTree='SOURCE_ROOT')
# Model localized resources as a PBXVariantGroup, as Xcode does.
localized_path='Resources/ja.lproj/Localizable.strings'
localized_file=refs[localized_path]
objects[localized_file]['name']='ja'
refs[localized_path]=add('localized-strings',isa='PBXVariantGroup',children=[localized_file],name='Localizable.strings',sourceTree='<group>')
app_product=add('app-product',isa='PBXFileReference',explicitFileType='wrapper.application',path='HangulStudy.app',sourceTree='BUILT_PRODUCTS_DIR',includeInIndex=0)
test_product=add('test-product',isa='PBXFileReference',explicitFileType='wrapper.cfbundle',path='HangulStudyTests.xctest',sourceTree='BUILT_PRODUCTS_DIR',includeInIndex=0)
ui_product=add('ui-product',isa='PBXFileReference',explicitFileType='wrapper.cfbundle',path='HangulStudyUITests.xctest',sourceTree='BUILT_PRODUCTS_DIR',includeInIndex=0)
products=add('products',isa='PBXGroup',children=[app_product,test_product,ui_product],name='Products',sourceTree='<group>')
groups=[]
for folder in ['App','Models','Services','Repositories','Views','ViewModels','Persistence','LearningEngine','Content','Utilities','Resources','Config','Tests']:
    members=[refs[f] for f in refs if f.startswith(folder+'/')]
    groups.append(add('group:'+folder,isa='PBXGroup',children=members,name=folder,sourceTree='<group>'))
main_group=add('main-group',isa='PBXGroup',children=groups+[products],sourceTree='<group>')
def phase(name,kind,files):
    builds=[add('build:'+name+':'+f,isa='PBXBuildFile',fileRef=refs[f]) for f in files]
    return add('phase:'+name,isa=kind,buildActionMask=2147483647,files=builds,runOnlyForDeploymentPostprocessing=0)
app_sources=phase('app-sources','PBXSourcesBuildPhase',app_files)
app_resources=phase('app-resources','PBXResourcesBuildPhase',resources)
app_frameworks=phase('app-frameworks','PBXFrameworksBuildPhase',[])
# Pin reviewed official SDK versions. Resolve with Xcode on macOS; no vendored binary.
packages=[]; package_products=[]
for slug,product,version in [('google-mobile-ads','GoogleMobileAds','13.11.0'),('google-user-messaging-platform','GoogleUserMessagingPlatform','3.1.0')]:
    package=add('package:'+slug,isa='XCRemoteSwiftPackageReference',repositoryURL='https://github.com/googleads/swift-package-manager-'+slug+'.git',requirement={'kind':'exactVersion','version':version})
    dependency=add('product:'+product,isa='XCSwiftPackageProductDependency',package=package,productName=product)
    packages.append(package); package_products.append(dependency)
    objects[app_frameworks]['files'].append(add('link:'+product,isa='PBXBuildFile',productRef=dependency))
test_sources=phase('test-sources','PBXSourcesBuildPhase',test_files)
test_resources=phase('test-resources','PBXResourcesBuildPhase',test_resource_files)
test_frameworks=phase('test-frameworks','PBXFrameworksBuildPhase',[])
ui_sources=phase('ui-sources','PBXSourcesBuildPhase',ui_files)
ui_resources=phase('ui-resources','PBXResourcesBuildPhase',ui_resource_files)
ui_frameworks=phase('ui-frameworks','PBXFrameworksBuildPhase',[])
script='set -eu\nsource_db="$SRCROOT/Resources/content.sqlite"\nmkdir -p "$TARGET_BUILD_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH"\ncp "$source_db" "$TARGET_BUILD_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH/content.sqlite"\n'
copy_content=add('copy-content',isa='PBXShellScriptBuildPhase',buildActionMask=2147483647,files=[],inputPaths=['$(SRCROOT)/Resources/content.sqlite'],outputPaths=['$(TARGET_BUILD_DIR)/$(UNLOCALIZED_RESOURCES_FOLDER_PATH)/content.sqlite'],name='Select content database',runOnlyForDeploymentPostprocessing=0,shellPath='/bin/sh',shellScript=script)
common={'SDKROOT':'iphoneos','IPHONEOS_DEPLOYMENT_TARGET':'16.0','SWIFT_VERSION':'5.0','CLANG_ENABLE_MODULES':'YES','CLANG_ENABLE_OBJC_ARC':'YES','SWIFT_STRICT_CONCURRENCY':'complete','ENABLE_USER_SCRIPT_SANDBOXING':'YES'}
app={'PRODUCT_NAME':'$(TARGET_NAME)','PRODUCT_BUNDLE_IDENTIFIER':'com.example.HangulStudy','GENERATE_INFOPLIST_FILE':'NO','INFOPLIST_FILE':'Resources/Info.plist','TARGETED_DEVICE_FAMILY':'1,2','CODE_SIGN_STYLE':'Automatic','CURRENT_PROJECT_VERSION':'1','MARKETING_VERSION':'0.1.0','OTHER_LDFLAGS':['$(inherited)','-lsqlite3'],'SWIFT_EMIT_LOC_STRINGS':'YES','LD_RUNPATH_SEARCH_PATHS':['$(inherited)','@executable_path/Frameworks']}
# Preserve an owner-selected team across deterministic regeneration. A team ID
# is configuration, never a certificate/private key or a claim of release access.
existing_project=ROOT/'HangulStudy.xcodeproj/project.pbxproj'
existing_project_text=existing_project.read_text() if existing_project.exists() else ''
teams=set(re.findall(r'"?DEVELOPMENT_TEAM"?\s*=\s*"?([A-Z0-9]{10})',existing_project_text))
if len(teams)>1: raise ValueError('Multiple signing teams: preserve per-target configuration before regenerating')
if teams: app['DEVELOPMENT_TEAM']=next(iter(teams))
test={'PRODUCT_NAME':'$(TARGET_NAME)','PRODUCT_BUNDLE_IDENTIFIER':'com.example.HangulStudyTests','GENERATE_INFOPLIST_FILE':'YES','TARGETED_DEVICE_FAMILY':'1,2','TEST_HOST':'$(BUILT_PRODUCTS_DIR)/HangulStudy.app/HangulStudy','BUNDLE_LOADER':'$(TEST_HOST)','LD_RUNPATH_SEARCH_PATHS':['$(inherited)','@executable_path/Frameworks','@loader_path/Frameworks'],'CODE_SIGN_STYLE':'Automatic','OTHER_LDFLAGS':['$(inherited)','-lsqlite3']}
test['IPHONEOS_DEPLOYMENT_TARGET']='17.0'
ui={'PRODUCT_NAME':'$(TARGET_NAME)','PRODUCT_BUNDLE_IDENTIFIER':'com.example.HangulStudyUITests','GENERATE_INFOPLIST_FILE':'YES','TARGETED_DEVICE_FAMILY':'1,2','TEST_TARGET_NAME':'HangulStudy','CODE_SIGN_STYLE':'Automatic','IPHONEOS_DEPLOYMENT_TARGET':'17.0','OTHER_LDFLAGS':['$(inherited)','-lsqlite3']}
def preserved_signing(name,config):
    # Both this writer and Xcode end each configuration object at two tabs.
    block=re.search(r'"?'+ident(name+config)+r'"?\s*(?:/\*.*?\*/\s*)?=\s*\{(.*?)\n\t\t\};',existing_project_text,re.S)
    if not block: return {}
    result={}
    for key in ['DEVELOPMENT_TEAM','CODE_SIGN_IDENTITY[sdk=macosx*]']:
        value=re.search(r'"?'+re.escape(key)+r'"?\s*=\s*("(?:[^"\\]|\\.)*"|[^;\s]+)\s*;',block.group(1))
        if value: result[key]=json.loads(value.group(1)) if value.group(1).startswith('"') else value.group(1)
    return result
def configs(name,settings):
    result=[]
    for config in ['Debug','Release']:
        opts=dict(settings)
        opts.update(preserved_signing(name,config))
        if config=='Debug': opts.update(SWIFT_OPTIMIZATION_LEVEL='-Onone',SWIFT_ACTIVE_COMPILATION_CONDITIONS='$(inherited) DEBUG',ENABLE_TESTABILITY='YES',DEBUG_INFORMATION_FORMAT='dwarf')
        else: opts.update(SWIFT_OPTIMIZATION_LEVEL='-O',SWIFT_COMPILATION_MODE='wholemodule',DEBUG_INFORMATION_FORMAT='dwarf-with-dsym')
        extra={'baseConfigurationReference':refs['Config/'+config+'.xcconfig']} if name=='app' else {}
        result.append(add(name+config,isa='XCBuildConfiguration',buildSettings=opts,name=config,**extra))
    return add(name+'config-list',isa='XCConfigurationList',buildConfigurations=result,defaultConfigurationIsVisible=0,defaultConfigurationName='Release')
app_target=add('app-target',isa='PBXNativeTarget',buildConfigurationList=configs('app',app),buildPhases=[app_sources,app_frameworks,app_resources,copy_content],buildRules=[],dependencies=[],packageProductDependencies=package_products,name='HangulStudy',productName='HangulStudy',productReference=app_product,productType='com.apple.product-type.application')
proxy=add('proxy',isa='PBXContainerItemProxy',containerPortal=ident('project'),proxyType=1,remoteGlobalIDString=app_target,remoteInfo='HangulStudy')
dependency=add('test-dependency',isa='PBXTargetDependency',target=app_target,targetProxy=proxy)
test_target=add('test-target',isa='PBXNativeTarget',buildConfigurationList=configs('test',test),buildPhases=[test_sources,test_frameworks,test_resources],buildRules=[],dependencies=[dependency],name='HangulStudyTests',productName='HangulStudyTests',productReference=test_product,productType='com.apple.product-type.bundle.unit-test')
ui_dependency=add('ui-dependency',isa='PBXTargetDependency',target=app_target,targetProxy=proxy)
ui_target=add('ui-target',isa='PBXNativeTarget',buildConfigurationList=configs('ui',ui),buildPhases=[ui_sources,ui_frameworks,ui_resources],buildRules=[],dependencies=[ui_dependency],name='HangulStudyUITests',productName='HangulStudyUITests',productReference=ui_product,productType='com.apple.product-type.bundle.ui-testing')
project=add('project',isa='PBXProject',attributes={'BuildIndependentTargetsInParallel':'YES','LastUpgradeCheck':'1500','TargetAttributes':{app_target:{'CreatedOnToolsVersion':'16.0','SystemCapabilities':{'com.apple.InAppPurchase':{'enabled':1}}},test_target:{'CreatedOnToolsVersion':'15.0','TestTargetID':app_target},ui_target:{'CreatedOnToolsVersion':'27.1','TestTargetID':app_target}}},buildConfigurationList=configs('project',common),compatibilityVersion='Xcode 14.0',developmentRegion='ja',hasScannedForEncodings=0,knownRegions=['ja','Base'],mainGroup=main_group,productRefGroup=products,projectDirPath='',projectRoot='',packageReferences=packages,targets=[app_target,test_target,ui_target])
project_dir=ROOT/'HangulStudy.xcodeproj'
project_dir.mkdir(exist_ok=True)
(project_dir/'project.pbxproj').write_text('// !$*UTF8*$!\n'+encode({'archiveVersion':'1','classes':{},'objectVersion':'56','objects':objects,'rootObject':project})+'\n')
schemes=project_dir/'xcshareddata/xcschemes'; schemes.mkdir(parents=True,exist_ok=True)
def ref(target,name,buildable): return f'<BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{target}" BuildableName="{buildable}" BlueprintName="{name}" ReferencedContainer="container:HangulStudy.xcodeproj"/>'
appref=ref(app_target,'HangulStudy','HangulStudy.app'); testref=ref(test_target,'HangulStudyTests','HangulStudyTests.xctest')
uiref=ref(ui_target,'HangulStudyUITests','HangulStudyUITests.xctest')
(schemes/'HangulStudy.xcscheme').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion="1500" version="1.3">
<BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES"><BuildActionEntries>
<BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES">{appref}</BuildActionEntry>
</BuildActionEntries></BuildAction>
<TestAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" shouldUseLaunchSchemeArgsEnv="YES"><Testables><TestableReference skipped="NO">{testref}</TestableReference><TestableReference skipped="NO">{uiref}</TestableReference></Testables></TestAction>
<LaunchAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" launchStyle="0" useCustomWorkingDirectory="NO" ignoresPersistentStateOnLaunch="NO" debugDocumentVersioning="YES" debugServiceExtension="internal" allowLocationSimulation="YES"><BuildableProductRunnable runnableDebuggingMode="0">{appref}</BuildableProductRunnable></LaunchAction>
<ProfileAction buildConfiguration="Release" shouldUseLaunchSchemeArgsEnv="YES" savedToolIdentifier="" useCustomWorkingDirectory="NO" debugDocumentVersioning="YES"><BuildableProductRunnable runnableDebuggingMode="0">{appref}</BuildableProductRunnable></ProfileAction>
<AnalyzeAction buildConfiguration="Debug"/><ArchiveAction buildConfiguration="Release" revealArchiveInOrganizer="YES"/>
</Scheme>''')
workspace=project_dir/'project.xcworkspace'; workspace.mkdir(exist_ok=True)
(workspace/'contents.xcworkspacedata').write_text('<?xml version="1.0" encoding="UTF-8"?><Workspace version="1.0"><FileRef location="self:"/></Workspace>')
print(f'Generated project: {len(app_files)} app Swift files, {len(test_files)} test files')

# Local purchase simulation is opt-in and never attached to the normal/archive scheme.
local_scheme=(schemes/'HangulStudy.xcscheme').read_text().replace('</LaunchAction>', '<StoreKitConfigurationFileReference identifier="../../Config/RemoveAds.storekit"/></LaunchAction>')
(schemes/'HangulStudy-StoreKit.xcscheme').write_text(local_scheme)

# Physical-device UI checks must never run tests that clear the purchase cache.
# Use the normal Release app/data namespace and only the UI automation bundle.
device_scheme=ET.fromstring((schemes/'HangulStudy.xcscheme').read_text())
device_test=device_scheme.find('TestAction'); device_test.set('buildConfiguration','Release')
device_testables=device_test.find('Testables')
for testable in list(device_testables):
    if testable.find('BuildableReference').get('BlueprintName')!='HangulStudyUITests':
        device_testables.remove(testable)
ET.indent(device_scheme,space='  ')
(schemes/'HangulStudy-DeviceUI.xcscheme').write_bytes(ET.tostring(device_scheme,encoding='utf-8',xml_declaration=True)+b'\n')
