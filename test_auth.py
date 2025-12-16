#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify GitHub CLI authentication and permissions
"""

import subprocess
import json
import platform
import sys

# Detect operating system
SYSTEM = platform.system()
GH_PATH = 'gh' if SYSTEM == 'Windows' else '/opt/homebrew/bin/gh'

def test_gh_installed():
    """Test if GitHub CLI is installed"""
    print("🔍 Testing GitHub CLI installation...")
    try:
        result = subprocess.run(
            [GH_PATH, '--version'],
            capture_output=True, text=True, check=True
        )
        print(f"✅ GitHub CLI installed: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ GitHub CLI not found: {e}")
        return False

def test_gh_auth():
    """Test if GitHub CLI is authenticated"""
    print("\n🔍 Testing GitHub CLI authentication...")
    try:
        result = subprocess.run(
            [GH_PATH, 'auth', 'status'],
            capture_output=True, text=True, check=True
        )
        print("✅ GitHub CLI authenticated")
        print(result.stderr)  # gh auth status outputs to stderr
        return True
    except Exception as e:
        print(f"❌ GitHub CLI not authenticated: {e}")
        return False

def test_list_repos():
    """Test if we can list repositories"""
    print("\n🔍 Testing repository listing...")
    try:
        result = subprocess.run(
            [GH_PATH, 'repo', 'list', '--limit', '3', 
             '--json', 'name,diskUsage,pushedAt,isPrivate'],
            capture_output=True, text=True, check=True
        )
        repos = json.loads(result.stdout)
        print(f"✅ Successfully listed {len(repos)} repositories")
        for repo in repos:
            print(f"   - {repo['name']} ({'Private' if repo['isPrivate'] else 'Public'})")
        return True
    except Exception as e:
        print(f"❌ Failed to list repositories: {e}")
        return False

def test_delete_scope():
    """Test if delete_repo scope is granted"""
    print("\n🔍 Testing delete_repo permission...")
    try:
        result = subprocess.run(
            [GH_PATH, 'auth', 'status', '-t'],
            capture_output=True, text=True, check=True
        )
        # Combine stdout and stderr
        output = result.stdout + result.stderr
        if 'delete_repo' in output:
            print("✅ delete_repo scope is granted")
            # Extract and show the scopes
            for line in output.split('\n'):
                if 'Token scopes' in line:
                    print(f"   {line.strip()}")
            return True
        else:
            print("⚠️  delete_repo scope NOT found")
            print("   Run: gh auth refresh -h github.com -s delete_repo")
            return False
    except Exception as e:
        print(f"⚠️  Could not verify delete_repo scope: {e}")
        return False

def test_create_and_delete():
    """Test creating and deleting a repository"""
    test_repo_name = "test-permissions-check"
    
    print(f"\n🔍 Testing create and delete workflow...")
    print(f"   Creating test repository: {test_repo_name}")
    
    # Create test repo
    try:
        subprocess.run(
            [GH_PATH, 'repo', 'create', test_repo_name, '--private'],
            check=True, capture_output=True, text=True
        )
        print(f"   ✅ Created {test_repo_name}")
    except Exception as e:
        print(f"   ❌ Failed to create repository: {e}")
        return False
    
    # Delete test repo
    try:
        subprocess.run(
            [GH_PATH, 'repo', 'delete', f'teadock/{test_repo_name}', '--yes'],
            check=True, capture_output=True, text=True
        )
        print(f"   ✅ Deleted {test_repo_name}")
        print("✅ Create and delete workflow successful!")
        return True
    except Exception as e:
        print(f"   ❌ Failed to delete repository: {e}")
        print(f"   ⚠️  You may need to manually delete: teadock/{test_repo_name}")
        return False

def main():
    print("=" * 60)
    print("GitHub Repository Manager - Authentication Test")
    print("=" * 60)
    
    results = {
        'gh_installed': test_gh_installed(),
        'gh_auth': test_gh_auth(),
        'list_repos': test_list_repos(),
        'delete_scope': test_delete_scope(),
        'create_delete': test_create_and_delete()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    all_passed = True
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test.replace('_', ' ').title()}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        print("✅ Your application is ready to use!")
        print("   You can delete repositories with a single click!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
