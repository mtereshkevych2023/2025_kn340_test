# GitHub Actions and Projects Integration

This repository is configured to integrate GitHub Actions workflows with GitHub Projects for better project management and automation.

## Overview

The integration consists of two main workflows:

### 1. Run Tests Workflow (`python-app.yml`)

This workflow runs on every push and pull request to the main branch. It:
- Installs dependencies using Poetry
- Runs linting with flake8
- Checks code formatting with black
- Runs tests with pytest
- **Reports workflow status to related issues**

#### Issue Status Reporting

The workflow automatically posts comments to issues that are referenced in commit messages (e.g., "Fix #123") or associated with pull requests. The comments include:
- Workflow status (success ✅ or failure ❌)
- Commit SHA
- Link to the workflow run

This helps track which commits and tests are related to specific issues.

### 2. Add to Project Workflow (`add-to-project.yml`)

This workflow automatically adds newly opened or reopened issues and pull requests to a GitHub Project board.

#### Configuration

To use this workflow, you need to:

1. **Create a GitHub Project**:
   - Go to your GitHub profile or organization
   - Click on "Projects" tab
   - Create a new project
   - Copy the project URL (e.g., `https://github.com/users/USERNAME/projects/1`)

2. **Configure the Project URL**:
   
   **Option A: Using Repository Variables (Recommended)**
   - Go to your repository Settings → Secrets and variables → Actions → Variables
   - Create a new variable named `PROJECT_URL`
   - Set its value to your project URL
   
   **Option B: Direct Configuration**
   - Edit `.github/workflows/add-to-project.yml`
   - Replace the `project-url` value with your actual project URL

3. **Permissions**:
   - The workflow requires `repository-projects: write` permission
   - This is already configured in the workflow file

## How It Works

### For Issues:

1. When you create or reopen an issue, the "Add to Project" workflow automatically adds it to your project board
2. When you reference an issue in a commit message (e.g., "Fix #5"), and push to main:
   - The "Run Tests" workflow runs
   - After completion, it posts a status comment to issue #5
   - The comment includes whether tests passed or failed and a link to the workflow run

### For Pull Requests:

1. When you create a pull request, it's automatically added to the project board
2. When the "Run Tests" workflow runs on the PR:
   - It posts a status comment to the PR
   - You can see the test results directly on the PR

## Example Usage

### Workflow in Action:

1. Create an issue: "Add new feature"
2. Create a branch: `feature/new-feature`
3. Make changes and commit: `git commit -m "Implement new feature for #1"`
4. Push and create PR: The tests run automatically
5. The workflow posts results to issue #1 and the PR
6. Both the issue and PR appear in your project board

## Benefits

- **Automated Tracking**: Issues and PRs are automatically added to projects
- **Test Status Visibility**: See test results directly on issues
- **Better Organization**: All work items are automatically organized in your project
- **Audit Trail**: Complete history of test runs related to each issue

## Customization

You can customize the workflows by:

- Modifying the triggers in `on:` sections
- Adding labels for automatic categorization
- Adjusting the status message format
- Adding more project automation rules

## Troubleshooting

If the workflows aren't working:

1. **Check Permissions**: Ensure the workflows have the necessary permissions
2. **Verify Project URL**: Make sure `PROJECT_URL` variable is set correctly
3. **Check Workflow Logs**: View the Actions tab to see detailed logs
4. **Token Permissions**: The `GITHUB_TOKEN` must have access to the project

For more information, see:
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
