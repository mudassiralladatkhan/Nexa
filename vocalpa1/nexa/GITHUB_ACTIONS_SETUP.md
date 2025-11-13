# 🚀 GitHub Actions APK Build Setup

## 📋 **Complete Setup Guide**

This guide will help you set up automated APK building for your Nexa Voice Assistant project using GitHub Actions.

---

## 🔧 **Prerequisites**

### **1. GitHub Repository**
- ✅ Push your Nexa project to: https://github.com/mudassiralladatkhan/Nexa
- ✅ Ensure the repository is public or you have GitHub Actions enabled

### **2. Project Structure**
Your repository should have this structure:
```
Nexa/
├── .github/
│   └── workflows/
│       ├── build-apk.yml          # Main build workflow
│       └── release-apk-fixed.yml  # Release workflow
├── mobile/                        # React Native app
│   ├── package.json
│   ├── index.js
│   ├── App.js
│   └── android/
│       ├── build.gradle
│       ├── gradlew
│       └── app/
├── backend/                       # Python backend
├── frontend/                      # Web frontend
└── shared/                        # Shared modules
```

---

## 🚀 **Setup Steps**

### **Step 1: Upload Workflow Files**

1. **Create the `.github/workflows/` directory** in your repository
2. **Upload these workflow files**:
   - `build-apk.yml` - Main build workflow
   - `release-apk-fixed.yml` - Release workflow

### **Step 2: Prepare Mobile App**

Ensure your `mobile/` directory has:
- ✅ `package.json` with React Native dependencies
- ✅ `index.js` entry point
- ✅ `android/` directory with Gradle build files
- ✅ `App.js` main component

### **Step 3: Configure Android Build**

Update `mobile/android/app/build.gradle`:
```gradle
android {
    compileSdkVersion 34
    buildToolsVersion "34.0.0"
    
    defaultConfig {
        applicationId "com.nexamobile"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }
    
    buildTypes {
        debug {
            debuggable true
        }
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

---

## 🎯 **How to Trigger Builds**

### **Automatic Builds**
- **Push to main/master**: Triggers debug APK build
- **Create Pull Request**: Triggers debug APK build
- **Create Release/Tag**: Triggers release APK build

### **Manual Builds**
1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **Build Nexa Android APK** workflow
4. Click **Run workflow**
5. Choose build type (debug/release)
6. Click **Run workflow**

---

## 📱 **Build Outputs**

### **Debug APK**
- **File**: `app-debug.apk`
- **Use**: Testing and development
- **Size**: ~25-35 MB
- **Signed**: Debug keystore

### **Release APK**
- **File**: `app-release-unsigned.apk`
- **Use**: Production distribution
- **Size**: ~20-30 MB (optimized)
- **Signed**: Unsigned (needs signing for Play Store)

---

## 📥 **Download APKs**

### **From Workflow Runs**
1. Go to **Actions** tab in your repository
2. Click on a completed workflow run
3. Scroll down to **Artifacts** section
4. Download `nexa-debug-apk` or `nexa-release-apk`

### **From Releases**
1. Go to **Releases** section in your repository
2. Find the latest release
3. Download APK files from **Assets** section

---

## 🔧 **Workflow Features**

### **Build Workflow (`build-apk.yml`)**
- ✅ **Multi-platform**: Runs on Ubuntu
- ✅ **Node.js 18**: Latest stable version
- ✅ **Java 17**: Required for Android builds
- ✅ **Android SDK 34**: Latest Android version
- ✅ **Gradle caching**: Faster builds
- ✅ **Artifact upload**: Easy APK download
- ✅ **Build summary**: Detailed build info

### **Release Workflow (`release-apk-fixed.yml`)**
- ✅ **Tag-triggered**: Automatic on version tags
- ✅ **Release creation**: Automatic GitHub releases
- ✅ **APK attachment**: APKs attached to releases
- ✅ **Release notes**: Automatic changelog
- ✅ **Dual builds**: Both debug and release APKs

---

## 🎯 **Usage Examples**

### **Create a Release**
```bash
# Tag a new version
git tag v1.0.0
git push origin v1.0.0

# This will automatically:
# 1. Trigger the release workflow
# 2. Build both debug and release APKs
# 3. Create a GitHub release
# 4. Attach APKs to the release
```

### **Manual Build**
1. Go to GitHub Actions
2. Select "Build Nexa Android APK"
3. Click "Run workflow"
4. Choose "release" for production APK
5. Download from Artifacts

---

## 📊 **Build Time & Resources**

### **Expected Build Times**
- **Debug APK**: ~8-12 minutes
- **Release APK**: ~10-15 minutes
- **Both**: ~12-18 minutes

### **GitHub Actions Usage**
- **Free tier**: 2,000 minutes/month
- **Cost per build**: ~10-15 minutes
- **Monthly capacity**: ~130-200 builds

---

## 🔍 **Troubleshooting**

### **Common Issues**

**Build Fails - Missing Dependencies**
```yaml
# Add to workflow if needed
- name: Install missing dependencies
  run: |
    npm install -g react-native-cli
    npm install -g @react-native-community/cli
```

**Gradle Build Fails**
```yaml
# Add Gradle daemon disable
- name: Build APK
  run: ./gradlew assembleDebug --no-daemon --stacktrace
```

**JavaScript Bundle Fails**
```yaml
# Ensure assets directory exists
- name: Create assets directory
  run: mkdir -p android/app/src/main/assets
```

### **Debug Steps**
1. Check workflow logs in Actions tab
2. Look for red ❌ steps
3. Expand error logs
4. Fix issues in your code
5. Push changes to trigger new build

---

## 🎉 **Success Indicators**

### **✅ Successful Build**
- All workflow steps show green ✅
- APK artifacts are available for download
- Build summary shows APK size and info
- No error messages in logs

### **📱 APK Ready**
- APK file downloads successfully
- File size is reasonable (20-35 MB)
- APK installs on Android device
- App launches and works correctly

---

## 🚀 **Next Steps**

1. **Push your code** to the GitHub repository
2. **Upload the workflow files** to `.github/workflows/`
3. **Trigger a manual build** to test
4. **Create a release tag** for automatic release
5. **Download and test** the generated APK

---

## 📋 **Checklist**

- [ ] Repository created at https://github.com/mudassiralladatkhan/Nexa
- [ ] Workflow files uploaded to `.github/workflows/`
- [ ] Mobile app structure is correct
- [ ] `package.json` has all dependencies
- [ ] Android build configuration is set
- [ ] First build triggered successfully
- [ ] APK downloaded and tested
- [ ] Release workflow tested with tag

---

**🎉 Your Nexa Voice Assistant will now build APKs automatically with every push!**

**GitHub Actions URL**: https://github.com/mudassiralladatkhan/Nexa/actions

---

**Status**: ✅ **READY FOR AUTOMATED APK BUILDS**  
**Build Time**: ~10-15 minutes per APK  
**Output**: Production-ready Android APK files  
**Distribution**: GitHub Releases + Artifacts
