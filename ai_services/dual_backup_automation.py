"""
Dual-Backup Automation System for 4UAI Platform
Automated synchronization between GitHub and Google Drive for enterprise data protection
"""
import os
import json
import logging
import shutil
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass
import hashlib

try:
    from github import Github
    import git
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

from google_drive_service import get_drive_service
from drive_folder_manager import get_folder_manager

logger = logging.getLogger(__name__)

@dataclass
class BackupItem:
    """Represents an item to be backed up"""
    local_path: str
    category: str  # 'code', 'ip', 'legal', 'docs'
    priority: str  # 'high', 'medium', 'low'
    file_type: str
    description: str
    last_modified: datetime
    file_hash: str

@dataclass
class BackupResult:
    """Result of backup operation"""
    success: bool
    github_url: Optional[str]
    drive_url: Optional[str]
    errors: List[str]
    warnings: List[str]

class DualBackupAutomation:
    """Enterprise dual-backup automation system"""
    
    def __init__(self):
        self.github_client = None
        self.drive_service = get_drive_service()
        self.folder_manager = get_folder_manager()
        self.backup_config = None
        self._initialize_services()
        
        # Define backup categories and their GitHub/Drive locations
        self.backup_categories = {
            'code': {
                'github_repo': '4uai-platform-code',
                'drive_folder': ['4UAI-Platform', 'Code-Backup'],
                'extensions': ['.py', '.js', '.ts', '.css', '.html', '.json', '.yaml', '.yml'],
                'priority': 'high'
            },
            'ip': {
                'github_repo': '4uai-intellectual-property',
                'drive_folder': ['4UAI-Platform', 'Intellectual-Property'],
                'extensions': ['.pdf', '.docx', '.doc', '.txt', '.md'],
                'priority': 'high'
            },
            'legal': {
                'github_repo': '4uai-legal-documents',
                'drive_folder': ['4UAI-Platform', 'Legal-Documents'],
                'extensions': ['.pdf', '.docx', '.doc', '.txt'],
                'priority': 'high'
            },
            'docs': {
                'github_repo': '4uai-documentation',
                'drive_folder': ['4UAI-Platform', 'Documentation'],
                'extensions': ['.md', '.txt', '.pdf', '.docx'],
                'priority': 'medium'
            },
            'config': {
                'github_repo': '4uai-configurations',
                'drive_folder': ['4UAI-Platform', 'Configurations'],
                'extensions': ['.json', '.yaml', '.yml', '.env', '.conf'],
                'priority': 'high'
            }
        }
    
    def _initialize_services(self):
        """Initialize GitHub and Drive services"""
        try:
            # Initialize GitHub client
            if GITHUB_AVAILABLE:
                github_token = os.getenv('GITHUB_TOKEN')
                if github_token:
                    self.github_client = Github(github_token)
                    logger.info("✅ GitHub client initialized")
                else:
                    logger.warning("⚠️ GitHub token not found")
            else:
                logger.warning("⚠️ GitHub libraries not available")
            
            # Verify Drive service
            if self.drive_service.is_authenticated:
                logger.info("✅ Google Drive service authenticated")
            else:
                logger.warning("⚠️ Google Drive not authenticated")
                
        except Exception as e:
            logger.error(f"Failed to initialize backup services: {e}")
    
    def setup_backup_repositories(self) -> Dict[str, bool]:
        """Set up GitHub repositories for each backup category"""
        if not self.github_client:
            return {"error": "GitHub client not available"}
        
        setup_results = {}
        
        try:
            user = self.github_client.get_user()
            logger.info(f"📡 Connected to GitHub as: {user.login}")
            
            for category, config in self.backup_categories.items():
                repo_name = config['github_repo']
                
                try:
                    # Check if repository exists
                    repo = user.get_repo(repo_name)
                    setup_results[category] = f"Repository {repo_name} already exists"
                    logger.info(f"📁 Found existing repository: {repo_name}")
                    
                except Exception:
                    # Create new repository
                    try:
                        repo = user.create_repo(
                            name=repo_name,
                            description=f"4UAI Platform {category.title()} Backup Repository",
                            private=True,  # Keep repositories private for security
                            auto_init=True
                        )
                        setup_results[category] = f"Created repository {repo_name}"
                        logger.info(f"✅ Created repository: {repo_name}")
                        
                        # Create README
                        readme_content = f"""# 4UAI Platform {category.title()} Backup

This repository contains automated backups of {category} files from the 4UAI platform.

## Automated Backup System
- **Category**: {category.title()}
- **Priority**: {config['priority'].title()}
- **File Types**: {', '.join(config['extensions'])}
- **Last Update**: {datetime.now().isoformat()}

## Security Notice
This repository contains sensitive {category} data and should remain private.
"""
                        repo.create_file(
                            "README.md",
                            "Initial commit with README",
                            readme_content
                        )
                        
                    except Exception as e:
                        setup_results[category] = f"Failed to create {repo_name}: {str(e)}"
                        logger.error(f"❌ Failed to create repository {repo_name}: {e}")
            
            return setup_results
            
        except Exception as e:
            logger.error(f"Failed to setup repositories: {e}")
            return {"error": str(e)}
    
    def scan_files_for_backup(self, base_path: str = ".") -> Dict[str, List[BackupItem]]:
        """Scan filesystem for files that need backup"""
        backup_items = {category: [] for category in self.backup_categories.keys()}
        
        try:
            base_path = Path(base_path)
            
            # Define important files/patterns to backup
            important_patterns = {
                'code': [
                    "*.py", "*.js", "*.ts", "*.css", "*.html", 
                    "requirements.txt", "package.json", "*.yaml", "*.yml"
                ],
                'ip': [
                    "*patent*", "*intellectual*", "*proprietary*", 
                    "*trademark*", "*copyright*"
                ],
                'legal': [
                    "*contract*", "*agreement*", "*legal*", 
                    "*terms*", "*privacy*", "*license*"
                ],
                'docs': [
                    "README*", "*.md", "*documentation*", 
                    "*manual*", "*guide*"
                ],
                'config': [
                    "*.env", "*.conf", "*.config", "*settings*",
                    "docker*", "*.toml"
                ]
            }
            
            # Scan files
            for file_path in base_path.rglob("*"):
                if file_path.is_file() and not self._should_ignore_file(file_path):
                    
                    # Categorize file
                    category = self._categorize_file(file_path, important_patterns)
                    
                    if category:
                        # Calculate file hash for change detection
                        file_hash = self._calculate_file_hash(file_path)
                        
                        backup_item = BackupItem(
                            local_path=str(file_path),
                            category=category,
                            priority=self.backup_categories[category]['priority'],
                            file_type=file_path.suffix.lower(),
                            description=f"{category.title()} file: {file_path.name}",
                            last_modified=datetime.fromtimestamp(file_path.stat().st_mtime),
                            file_hash=file_hash
                        )
                        
                        backup_items[category].append(backup_item)
            
            # Log scan results
            total_files = sum(len(items) for items in backup_items.values())
            logger.info(f"📊 Scanned {total_files} files for backup:")
            for category, items in backup_items.items():
                if items:
                    logger.info(f"   {category}: {len(items)} files")
            
            return backup_items
            
        except Exception as e:
            logger.error(f"Failed to scan files: {e}")
            return {category: [] for category in self.backup_categories.keys()}
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored during backup"""
        ignore_patterns = [
            '__pycache__', '.git', '.gitignore', 'node_modules',
            '.env.local', '.DS_Store', '*.log', '*.tmp',
            '.pytest_cache', '.coverage', 'coverage.xml'
        ]
        
        file_str = str(file_path)
        return any(pattern in file_str for pattern in ignore_patterns)
    
    def _categorize_file(self, file_path: Path, patterns: Dict[str, List[str]]) -> Optional[str]:
        """Categorize file based on extension and name patterns"""
        file_name = file_path.name.lower()
        file_ext = file_path.suffix.lower()
        
        # Check each category
        for category, config in self.backup_categories.items():
            # Check by extension
            if file_ext in config['extensions']:
                return category
            
            # Check by name patterns
            if category in patterns:
                for pattern in patterns[category]:
                    pattern_clean = pattern.replace('*', '').lower()
                    if pattern_clean in file_name:
                        return category
        
        return None
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file for change detection"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return ""
    
    def backup_to_github(self, items: List[BackupItem], category: str) -> Tuple[bool, List[str], str]:
        """Backup files to GitHub repository"""
        if not self.github_client:
            return False, ["GitHub client not available"], ""
        
        try:
            user = self.github_client.get_user()
            repo_name = self.backup_categories[category]['github_repo']
            repo = user.get_repo(repo_name)
            
            backup_errors = []
            files_backed_up = 0
            
            for item in items:
                try:
                    # Read file content
                    with open(item.local_path, 'rb') as f:
                        content = f.read()
                    
                    # Create relative path for GitHub
                    relative_path = Path(item.local_path).name
                    
                    # Check if file already exists
                    try:
                        existing_file = repo.get_contents(relative_path)
                        # Update existing file
                        repo.update_file(
                            path=relative_path,
                            message=f"Update {relative_path} - {datetime.now().isoformat()}",
                            content=content,
                            sha=existing_file.sha
                        )
                    except Exception:
                        # Create new file
                        repo.create_file(
                            path=relative_path,
                            message=f"Add {relative_path} - {datetime.now().isoformat()}",
                            content=content
                        )
                    
                    files_backed_up += 1
                    logger.info(f"📤 Backed up to GitHub: {relative_path}")
                    
                except Exception as e:
                    error_msg = f"Failed to backup {item.local_path}: {str(e)}"
                    backup_errors.append(error_msg)
                    logger.error(error_msg)
            
            repo_url = repo.html_url
            logger.info(f"✅ GitHub backup complete: {files_backed_up} files backed up to {repo_url}")
            
            return len(backup_errors) == 0, backup_errors, repo_url
            
        except Exception as e:
            error_msg = f"GitHub backup failed: {str(e)}"
            logger.error(error_msg)
            return False, [error_msg], ""
    
    def backup_to_drive(self, items: List[BackupItem], category: str) -> Tuple[bool, List[str], str]:
        """Backup files to Google Drive"""
        if not self.drive_service.is_authenticated:
            return False, ["Google Drive not authenticated"], ""
        
        try:
            # Get or create category folder
            folder_path = self.backup_categories[category]['drive_folder']
            folder_id = self.folder_manager._get_folder_id_by_path(folder_path)
            
            if not folder_id:
                return False, [f"Failed to create Drive folder: {'/'.join(folder_path)}"], ""
            
            backup_errors = []
            files_backed_up = 0
            drive_url = f"https://drive.google.com/drive/folders/{folder_id}"
            
            for item in items:
                try:
                    # Upload file to Drive
                    result = self.drive_service.upload_file(
                        file_path=item.local_path,
                        folder_id=folder_id,
                        file_name=f"{Path(item.local_path).name}"
                    )
                    
                    if result.success:
                        files_backed_up += 1
                        logger.info(f"📤 Backed up to Drive: {item.local_path}")
                    else:
                        backup_errors.append(f"Drive upload failed: {result.error_message}")
                    
                except Exception as e:
                    error_msg = f"Failed to backup {item.local_path} to Drive: {str(e)}"
                    backup_errors.append(error_msg)
                    logger.error(error_msg)
            
            logger.info(f"✅ Drive backup complete: {files_backed_up} files backed up")
            
            return len(backup_errors) == 0, backup_errors, drive_url
            
        except Exception as e:
            error_msg = f"Drive backup failed: {str(e)}"
            logger.error(error_msg)
            return False, [error_msg], ""
    
    def execute_dual_backup(self, base_path: str = ".") -> Dict[str, BackupResult]:
        """Execute complete dual backup process"""
        logger.info("🚀 Starting dual backup automation...")
        
        results = {}
        
        try:
            # 1. Scan files for backup
            backup_items = self.scan_files_for_backup(base_path)
            
            # 2. Setup repositories if needed
            if self.github_client:
                repo_setup = self.setup_backup_repositories()
                logger.info(f"📁 Repository setup: {repo_setup}")
            
            # 3. Execute backup for each category
            for category, items in backup_items.items():
                if not items:
                    results[category] = BackupResult(
                        success=True,
                        github_url=None,
                        drive_url=None,
                        errors=[],
                        warnings=[f"No {category} files found"]
                    )
                    continue
                
                logger.info(f"🔄 Backing up {len(items)} {category} files...")
                
                # Backup to GitHub
                github_success, github_errors, github_url = self.backup_to_github(items, category)
                
                # Backup to Drive
                drive_success, drive_errors, drive_url = self.backup_to_drive(items, category)
                
                # Create result
                all_errors = github_errors + drive_errors
                warnings = []
                
                if not github_success:
                    warnings.append("GitHub backup had issues")
                if not drive_success:
                    warnings.append("Drive backup had issues")
                
                results[category] = BackupResult(
                    success=github_success and drive_success,
                    github_url=github_url if github_success else None,
                    drive_url=drive_url if drive_success else None,
                    errors=all_errors,
                    warnings=warnings
                )
            
            # 4. Generate backup report
            self._generate_backup_report(results)
            
            logger.info("✅ Dual backup automation completed")
            return results
            
        except Exception as e:
            logger.error(f"Dual backup failed: {e}")
            return {"error": BackupResult(False, None, None, [str(e)], [])}
    
    def _generate_backup_report(self, results: Dict[str, BackupResult]):
        """Generate backup completion report"""
        total_categories = len([r for r in results.values() if isinstance(r, BackupResult)])
        successful_categories = len([r for r in results.values() if isinstance(r, BackupResult) and r.success])
        
        logger.info("📊 BACKUP REPORT")
        logger.info("=" * 50)
        logger.info(f"Categories processed: {total_categories}")
        logger.info(f"Successful backups: {successful_categories}")
        logger.info(f"Success rate: {(successful_categories/total_categories*100):.1f}%")
        logger.info("")
        
        for category, result in results.items():
            if isinstance(result, BackupResult):
                status = "✅" if result.success else "❌"
                logger.info(f"{status} {category.upper()}")
                if result.github_url:
                    logger.info(f"   GitHub: {result.github_url}")
                if result.drive_url:
                    logger.info(f"   Drive: {result.drive_url}")
                if result.errors:
                    logger.info(f"   Errors: {len(result.errors)}")
                if result.warnings:
                    logger.info(f"   Warnings: {len(result.warnings)}")
        
        logger.info("=" * 50)
    
    def get_backup_status(self) -> Dict[str, Any]:
        """Get current backup system status"""
        status = {
            "github_connected": bool(self.github_client),
            "drive_connected": self.drive_service.is_authenticated,
            "categories_configured": len(self.backup_categories),
            "last_backup": None,  # Could be stored in database
            "repositories": {},
            "drive_folders": {}
        }
        
        # Check GitHub repositories
        if self.github_client:
            try:
                user = self.github_client.get_user()
                for category, config in self.backup_categories.items():
                    repo_name = config['github_repo']
                    try:
                        repo = user.get_repo(repo_name)
                        status["repositories"][category] = {
                            "name": repo_name,
                            "url": repo.html_url,
                            "private": repo.private,
                            "last_updated": repo.updated_at.isoformat()
                        }
                    except Exception:
                        status["repositories"][category] = {"status": "not_found"}
            except Exception as e:
                status["github_error"] = str(e)
        
        return status

# Global instance
backup_automation = None

def get_backup_automation() -> DualBackupAutomation:
    """Get or create backup automation instance"""
    global backup_automation
    if backup_automation is None:
        backup_automation = DualBackupAutomation()
    return backup_automation