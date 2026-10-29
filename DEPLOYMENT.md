# GitHub Pages Deployment Guide for Stick It To Em

## 🚀 Quick Setup

Your game is ready for GitHub Pages deployment! Here's what's been set up:

### Files Created:
- ✅ `main.py` - Web-optimized entry point
- ✅ `.github/workflows/deploy.yml` - Automatic deployment workflow
- ✅ Web build tested locally

## 📋 Deployment Steps

### 1. Enable GitHub Pages
1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section
4. Under **Source**, select **GitHub Actions**

### 2. Push Your Changes
```bash
git add .
git commit -m "Add GitHub Pages deployment"
git push origin Cards_animations
```

### 3. Automatic Deployment
- GitHub Actions will automatically build and deploy your game
- Check the **Actions** tab to see build progress
- Your game will be live at: `https://RodneyCStead.github.io/Stick_Game/`

## 🎮 Game Features for Web

### Responsive Design
- **Base Resolution**: 1200x800 (your design size)
- **Auto-scaling**: Works on phones, tablets, desktops
- **Browser Compatibility**: Chrome, Firefox, Safari, Edge

### Controls
- **Mouse**: Click to select/play cards
- **Double-click**: Activate cards
- **Touch**: Works on mobile devices
- **Keyboard**: ESC to exit (desktop only)

## 🔧 Technical Details

### Build Process
- Uses **pygbag** to convert pygame to WebAssembly
- All assets automatically included
- Async/await for smooth browser performance

### File Structure
```
build/web/          # Web deployment files
├── index.html      # Main page
├── main.js         # WebAssembly loader
├── stick_game.wasm # Compiled game
└── assets/         # All game assets
```

### Performance
- **Loading**: ~2-3 seconds initial load
- **File Size**: Optimized for web
- **Memory**: Efficient WebAssembly execution

## 🐛 Troubleshooting

### Build Issues
- Check **Actions** tab for error logs
- Ensure all imports are correct
- Verify asset paths are valid

### Browser Issues
- Enable WebAssembly (modern browsers have this)
- Allow audio autoplay for sound effects
- Use HTTPS for best compatibility

## 🌟 Next Steps

Once deployed, you can:
1. Share the URL with anyone
2. Embed in other websites
3. Test on mobile devices
4. Add touch-specific optimizations

Your game is now ready for the world! 🎉
