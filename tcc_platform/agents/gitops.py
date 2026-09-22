import sys
import os
import uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from tools.json_editor import patch_rule

def run_gitops(state):
    print("--- GITOPS NODE ---")
    
    target_rule = state.get("target_rule")
    patch_data = state.get("patch_data")
    
    if not target_rule or not patch_data:
        return {"status": "GitOps skipped."}
        
    program = target_rule["program"]
    rule_index = target_rule["rule_index"]
    
    # 1. Apply patch locally
    try:
        updated_rule = patch_rule(program, rule_index, patch_data)
    except Exception as e:
        return {"status": f"GitOps Error (Local Patch): {str(e)}"}
        
    # 2. Push to GitHub if token is present
    github_token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("GITHUB_REPO", "mock-org/tcc-config")
    
    if github_token:
        try:
            from github import Github
            g = Github(github_token)
            repo = g.get_repo(repo_name)
            
            file_path = f"repo/programs/{program}.json"
            
            # Read local patched file
            with open(file_path, "r") as f:
                new_content = f.read()
                
            branch_name = f"update-{program.lower()}-{uuid.uuid4().hex[:6]}"
            main_ref = repo.get_git_ref("heads/main")
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_ref.object.sha)
            
            contents = repo.get_contents(file_path, ref="main")
            repo.update_file(contents.path, f"Update {program} config", new_content, contents.sha, branch=branch_name)
            
            pr = repo.create_pull(title=f"Update config for {program}", body="Automated configuration update via TCC Config Platform.", head=branch_name, base="main")
            
            print(f"Raised Live PR: {pr.html_url}")
            return {"pr_url": pr.html_url, "status": "GitOps Live PR Created."}
        except Exception as e:
            print(f"GitHub API Error: {e}")
            return {"status": f"GitOps Live PR Failed: {str(e)}"}
    else:
        # Fallback to Mock
        pr_id = str(uuid.uuid4())[:8]
        pr_url = f"https://github.com/{repo_name}/pull/{pr_id}"
        print(f"Committed change locally and raised mock PR: {pr_url} (No GITHUB_TOKEN found)")
        
        return {
            "pr_url": pr_url,
            "status": "GitOps Mock PR Created."
        }
