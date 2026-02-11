# Git Workflow & Branch Protection

To prevent team members from pushing code directly to the main branch and force them to use Pull Requests (PRs), you need to configure **Branch Protection Rules**.

## 1. The Concept
*   **Main Branch (`main` / `master`)**: Read-only for direct pushes. Only accepts merges from PRs.
*   **Feature Branches (`feature/login`, `fix/bug-123`)**: Developers push here.
*   **Pull Request**: A request to merge a feature branch into `main`. This is where code review happens.

## 2. Setting up on GitHub

1.  Go to your repository on GitHub.
2.  Click **Settings** > **Branches**.
3.  Click **Add branch protection rule**.
4.  **Branch name pattern**: `main`
5.  Check the following boxes:
    *   **[x] Require a pull request before merging**: This ensures no one can push directly.
    *   **[x] Require approvals**: (Optional but recommended) Set to 1 or 2. This forces someone else to review the code.
    *   **[x] Require status checks to pass before merging**: (Best Practice) This ensures your CI (tests) passes before code can land.
    *   **[x] Do not allow bypassing the above settings**: Ensures admins (you) play by the rules too.

## 3. Developer Workflow

With these rules in place, if a developer tries this:
```bash
git checkout main
git add .
git commit -m "fixed stuff"
git push origin main
```
❌ **They will get an error:** `remote: error: GH006: Protected branch update failed`

**Correct Workflow:**
1.  **Branch**: `git checkout -b feature/my-cool-feature`
2.  **Work**: Write code, commit.
3.  **Push**: `git push origin feature/my-cool-feature`
4.  **PR**: Go to GitHub and open a Pull Request.
5.  **Merge**: Once approved, click "Merge" in the UI.
