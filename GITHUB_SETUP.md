# Create GitHub Repository - Step by Step

Since the repository doesn't exist yet on GitHub, follow these steps to create it:

## Step 1: Create Repository on GitHub

1. Go to: **https://github.com/new**
2. Fill in the form:
   - **Repository name:** `Investments`
   - **Description:** `Tech Investment News Crawler with Web Interface - Multi-source news aggregation, relevance analysis, and web browsing interface`
   - **Visibility:** Choose `Public` or `Private` (your preference)
   - **Initialize with:**
     - ❌ Do NOT check "Add a README.md" (we have one)
     - ❌ Do NOT check "Add .gitignore" (we have one)
     - ❌ Do NOT check "Add license" (optional)

3. Click **"Create repository"**

## Step 2: After Creation

GitHub will show you a page with commands. Copy and run these commands in your terminal:

```bash
cd c:\Users\sfaith\Dev\Investments
git remote add origin https://github.com/sfaith5125/Investments.git
git branch -M main
git push -u origin main
```

## Full Command Sequence

Here's the complete set of commands to run (copy and paste into PowerShell):

```powershell
cd c:\Users\sfaith\Dev\Investments
git remote add origin https://github.com/sfaith5125/Investments.git
git branch -M main
git push -u origin main
```

## What Each Command Does

| Command | Purpose |
|---------|---------|
| `git remote add origin ...` | Links your local repo to GitHub |
| `git branch -M main` | Renames your branch to `main` |
| `git push -u origin main` | Pushes all commits to GitHub |

## If You Get Prompted for Password

GitHub might ask for authentication. You have two options:

### Option A: Personal Access Token (Recommended)
1. Go to: https://github.com/settings/tokens/new
2. Create a "Personal Access Token" with these scopes:
   - `repo` (full control of private repositories)
3. Copy the token (you'll only see it once!)
4. When git asks for password, paste the token
5. Windows will remember it for future pushes

### Option B: SSH Key
If you prefer SSH (more secure):
1. Generate SSH key: `ssh-keygen -t ed25519 -C "your@email.com"`
2. Add to GitHub: https://github.com/settings/keys
3. Change remote URL: `git remote set-url origin git@github.com:sfaith5125/Investments.git`
4. Then push: `git push -u origin main`

## Expected Output

After successful push, you should see:
```
Enumerating objects: 43, done.
Counting objects: 100% (43/43), done.
Delta compression using up to 8 threads
Compressing objects: 100% (38/38), done.
Writing objects: 100% (43/43), 95.68 KiB | 2.39 MiB/s, done.
Total 43 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/sfaith5125/Investments.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## Current Git Status

Your local git repo is ready:
```
✅ Repository initialized
✅ 42 files committed
✅ Commit: "Initial commit: Tech Investment News Crawler with web interface"
✅ Waiting for remote: GitHub repository to be created
```

## Next Steps

1. **Create repo on GitHub** → https://github.com/new
2. **Run the push commands** (copy from above)
3. **Verify on GitHub** → Visit https://github.com/sfaith5125/Investments

---

**Need help?** Run these commands one at a time and let me know if you hit any errors!
