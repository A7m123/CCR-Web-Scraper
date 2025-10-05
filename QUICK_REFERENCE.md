# 🎯 CCR Scraper - Quick Reference

## ⚡ Quick Commands

```bash
# Install
pip install -r requirements.txt

# Run (Default: scrapes configured pages)
python scraper_bulk.py

# View Data
python view_data.py

# Git Commands
git status
git log --oneline
```

---

## 📁 File Guide

| File | What It Does |
|------|--------------|
| `scraper_bulk.py` | **Main scraper** - Use this! |
| `config.json` | Settings (pages, format, etc.) |
| `view_data.py` | View scraped data |
| `PROJECT_SUMMARY.md` | **Show this to your boss first** |
| `START_HERE.md` | Step-by-step guide |
| `README.md` | Quick start |
| `SHARE_INSTRUCTIONS.md` | How to share this repo |

---

## ⚙️ Config Quick Edit

Edit `config.json`:

```json
{
  "pagination": {
    "max_pages": 100    // ← Change this number
  },
  "output": {
    "format": "excel"   // or "csv"
  }
}
```

**Common Values:**
- `100` = Test run (~10 minutes)
- `1000` = Small dataset (~1 hour)
- `10000` = Medium dataset (~6 hours)
- `200000` = Full dataset (~10 days)

---

## 📊 Output Files

Files created automatically:

```
ccr_checkpoint_page10_20251005_143000.xlsx   ← Every 10 pages
ccr_checkpoint_page20_20251005_143500.xlsx
ccr_final_20251005_150000.xlsx               ← Final output
```

---

## 🚦 Status Indicators

While running, you'll see:

```bash
[Page 5/100] ✓ Got 8 records | Total: 40     ← Success
[Page 6/100] ✗ No data (failure 1/3)          ← Temporary issue
[Page 10/100] 💾 CHECKPOINT SAVED              ← Auto-save
```

---

## 🛑 Stop Scraper

**Press**: `Ctrl + C`

**Result**: Data saved automatically to `ccr_interrupted_*.xlsx`

---

## 🎯 For Your Boss

**Show these files first:**
1. `PROJECT_SUMMARY.md` - Executive overview
2. Sample Excel output file
3. `START_HERE.md` - Usage guide

---

## 📦 Share Options

1. **ZIP File**: Right-click folder → Send to → Compressed folder
2. **GitHub**: `git remote add origin <url>` then `git push`
3. **Email**: Attach ZIP with PROJECT_SUMMARY.md
4. **Cloud**: Upload to Google Drive/OneDrive

See `SHARE_INSTRUCTIONS.md` for details.

---

## ✅ Pre-Run Checklist

- [ ] Installed Python 3.8+
- [ ] Ran `pip install -r requirements.txt`
- [ ] Chrome browser installed
- [ ] Internet connection stable
- [ ] Edited `config.json` if needed
- [ ] Computer sleep mode disabled (for long runs)

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Browser closes | Increase `page_load_delay` to 3-4 |
| No data | Check internet, wait, retry |
| Slow speed | Close other apps, check connection |
| Errors | See START_HERE.md troubleshooting section |

---

## 📈 Stats

- **Speed**: ~50 records/minute
- **Total Data**: ~764,000 records
- **Pages**: ~152,849 pages
- **Full Run**: ~10 days

---

## 🎓 Support

1. Check `START_HERE.md` (detailed guide)
2. Check `README_FULL.md` (technical docs)
3. Check error messages in terminal
4. Check `config.json` settings

---

## 🏆 Git Commands

```bash
# View history
git log --oneline

# Check status
git status

# Create ZIP backup
git archive -o backup.zip HEAD

# Share on GitHub
git remote add origin <your-github-url>
git push -u origin master
```

---

**Quick Start**: `python scraper_bulk.py` 🚀

**Last Updated**: October 5, 2025
