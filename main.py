import re
import sys
import json
import csv
import argparse
from typing import List, Tuple, Dict, Set
from pathlib import Path
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class EmailValidator:
    """
    Main Email Validation Class
    Handles validation logic, domain management, and batch processing
    """

    def __init__(self, whitelist_file: str = "domain_whitelist.json"):
        self.whitelist_file = Path(whitelist_file)
        self.domain_whitelist = self._load_whitelist()

        # Comprehensive email regex pattern
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )

        # Advanced pattern for stricter validation
        self.strict_pattern = re.compile(
            r'^[a-zA-Z0-9](?:[a-zA-Z0-9._-]*[a-zA-Z0-9])?@'
            r'[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?'
            r'(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)*$'
        )

    def _load_whitelist(self) -> Set[str]:
        """Load domain whitelist from JSON file"""
        try:
            if self.whitelist_file.exists():
                with open(self.whitelist_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('domains', []))
            return set()
        except (json.JSONDecodeError, FileNotFoundError):
            return set()

    def _save_whitelist(self) -> None:
        """Save domain whitelist to JSON file"""
        try:
            data = {
                'domains': list(self.domain_whitelist),
                'last_updated': datetime.now().isoformat(),
                'total_domains': len(self.domain_whitelist)
            }
            with open(self.whitelist_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"{Colors.RED}Error saving whitelist: {e}{Colors.RESET}")

    def validate_format(self, email: str, strict: bool = False) -> bool:
        """
        Validate email format using regex

        Args:
            email: Email address to validate
            strict: Use stricter validation pattern

        Returns:
            bool: True if format is valid
        """
        if not email or not isinstance(email, str):
            return False

        email = email.strip().lower()
        pattern = self.strict_pattern if strict else self.email_pattern
        return bool(pattern.match(email))

    def validate_domain(self, email: str) -> bool:
        """
        Check if email domain is in whitelist

        Args:
            email: Email address to check

        Returns:
            bool: True if domain is whitelisted or whitelist is empty
        """
        if not self.domain_whitelist:  # No whitelist = all domains allowed
            return True

        try:
            domain = email.split('@')[1].lower()
            return domain in self.domain_whitelist
        except IndexError:
            return False

    def validate_email(self, email: str, strict: bool = False) -> Tuple[bool, str]:
        """
        Complete email validation (format + domain)

        Args:
            email: Email address to validate
            strict: Use strict format validation

        Returns:
            Tuple[bool, str]: (is_valid, reason)
        """
        if not self.validate_format(email, strict):
            return False, "Invalid email format"

        if not self.validate_domain(email):
            domain = email.split('@')[1] if '@' in email else 'unknown'
            return False, f"Domain '{domain}' not in whitelist"

        return True, "Valid email"

    def batch_validate(self, emails: List[str], strict: bool = False) -> Dict[str, Dict]:
        """
        Validate multiple emails at once

        Args:
            emails: List of email addresses
            strict: Use strict validation

        Returns:
            Dict with validation results
        """
        results = {
            'valid': [],
            'invalid': [],
            'summary': {
                'total': len(emails),
                'valid_count': 0,
                'invalid_count': 0,
                'validation_rate': 0.0
            }
        }

        for email in emails:
            email = email.strip()
            if not email:
                continue

            is_valid, reason = self.validate_email(email, strict)

            entry = {
                'email': email,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }

            if is_valid:
                results['valid'].append(entry)
                results['summary']['valid_count'] += 1
            else:
                results['invalid'].append(entry)
                results['summary']['invalid_count'] += 1

        # Calculate validation rate
        total = results['summary']['valid_count'] + results['summary']['invalid_count']
        if total > 0:
            results['summary']['validation_rate'] = (
                    results['summary']['valid_count'] / total * 100
            )

        return results

    def add_domain(self, domain: str) -> bool:
        """Add domain to whitelist"""
        domain = domain.strip().lower()
        if domain and domain not in self.domain_whitelist:
            self.domain_whitelist.add(domain)
            self._save_whitelist()
            return True
        return False

    def remove_domain(self, domain: str) -> bool:
        """Remove domain from whitelist"""
        domain = domain.strip().lower()
        if domain in self.domain_whitelist:
            self.domain_whitelist.remove(domain)
            self._save_whitelist()
            return True
        return False

    def list_domains(self) -> List[str]:
        """Get sorted list of whitelisted domains"""
        return sorted(list(self.domain_whitelist))

    def clear_whitelist(self) -> int:
        """Clear all domains from whitelist"""
        count = len(self.domain_whitelist)
        self.domain_whitelist.clear()
        self._save_whitelist()
        return count

    def export_results(self, results: Dict, filename: str = None) -> str:
        """Export validation results to CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"email_validation_{timestamp}.csv"

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Email', 'Status', 'Reason', 'Timestamp'])

                for email_data in results['valid']:
                    writer.writerow([
                        email_data['email'],
                        'Valid',
                        email_data['reason'],
                        email_data['timestamp']
                    ])

                for email_data in results['invalid']:
                    writer.writerow([
                        email_data['email'],
                        'Invalid',
                        email_data['reason'],
                        email_data['timestamp']
                    ])

            return filename
        except Exception as e:
            print(f"{Colors.RED}Export failed: {e}{Colors.RESET}")
            return None


def print_banner():
    """Display application banner"""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    Email Validation Checker                 ║
║                         Version 1.0.0                       ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
    """
    print(banner)


def print_results(results: Dict):
    """Print validation results with colors"""
    summary = results['summary']

    print(f"\n{Colors.BOLD}📊 Validation Summary{Colors.RESET}")
    print(f"{'=' * 50}")
    print(f"Total Emails:     {Colors.BLUE}{summary['total']}{Colors.RESET}")
    print(f"Valid Emails:     {Colors.GREEN}{summary['valid_count']}{Colors.RESET}")
    print(f"Invalid Emails:   {Colors.RED}{summary['invalid_count']}{Colors.RESET}")
    print(f"Success Rate:     {Colors.PURPLE}{summary['validation_rate']:.1f}%{Colors.RESET}")

    if results['valid']:
        print(f"\n{Colors.GREEN}✅ Valid Emails:{Colors.RESET}")
        for item in results['valid']:
            print(f"  • {item['email']}")

    if results['invalid']:
        print(f"\n{Colors.RED}❌ Invalid Emails:{Colors.RESET}")
        for item in results['invalid']:
            print(f"  • {item['email']} - {Colors.YELLOW}{item['reason']}{Colors.RESET}")


def parse_email_input(input_str: str) -> List[str]:
    """Parse email input supporting multiple separators"""
    separators = [',', ';', ' ', '\n', '\t']
    emails = [input_str]

    for sep in separators:
        new_emails = []
        for email in emails:
            new_emails.extend(email.split(sep))
        emails = new_emails

    return [email.strip() for email in emails if email.strip()]


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Email Validation Checker - Validate emails with domain whitelisting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s validate "user@example.com"
  %(prog)s validate "user1@test.com,user2@demo.com" --strict
  %(prog)s domain add "company.com"
  %(prog)s domain list
  %(prog)s batch emails.txt --export results.csv
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate email addresses')
    validate_parser.add_argument('emails', help='Email(s) to validate (comma/space separated)')
    validate_parser.add_argument('--strict', action='store_true', help='Use strict validation')
    validate_parser.add_argument('--export', help='Export results to CSV file')

    # Domain management
    domain_parser = subparsers.add_parser('domain', help='Manage domain whitelist')
    domain_subparsers = domain_parser.add_subparsers(dest='domain_action')

    domain_add = domain_subparsers.add_parser('add', help='Add domain to whitelist')
    domain_add.add_argument('domain', help='Domain to add')

    domain_remove = domain_subparsers.add_parser('remove', help='Remove domain from whitelist')
    domain_remove.add_argument('domain', help='Domain to remove')

    domain_subparsers.add_parser('list', help='List all whitelisted domains')
    domain_subparsers.add_parser('clear', help='Clear all domains from whitelist')

    # Batch processing
    batch_parser = subparsers.add_parser('batch', help='Validate emails from file')
    batch_parser.add_argument('file', help='Text file with emails (one per line)')
    batch_parser.add_argument('--strict', action='store_true', help='Use strict validation')
    batch_parser.add_argument('--export', help='Export results to CSV file')

    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        return

    validator = EmailValidator()

    if args.command == 'validate':
        print_banner()
        emails = parse_email_input(args.emails)
        results = validator.batch_validate(emails, strict=args.strict)
        print_results(results)

        if args.export:
            exported_file = validator.export_results(results, args.export)
            if exported_file:
                print(f"\n{Colors.GREEN}📄 Results exported to: {exported_file}{Colors.RESET}")

    elif args.command == 'domain':
        if args.domain_action == 'add':
            if validator.add_domain(args.domain):
                print(f"{Colors.GREEN}✅ Added '{args.domain}' to whitelist{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}⚠️  Domain '{args.domain}' already exists{Colors.RESET}")

        elif args.domain_action == 'remove':
            if validator.remove_domain(args.domain):
                print(f"{Colors.GREEN}✅ Removed '{args.domain}' from whitelist{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ Domain '{args.domain}' not found{Colors.RESET}")

        elif args.domain_action == 'list':
            domains = validator.list_domains()
            if domains:
                print(f"\n{Colors.BOLD}📋 Whitelisted Domains ({len(domains)}){Colors.RESET}")
                print("=" * 40)
                for i, domain in enumerate(domains, 1):
                    print(f"{i:2}. {Colors.CYAN}{domain}{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}📝 No domains in whitelist (all domains allowed){Colors.RESET}")

        elif args.domain_action == 'clear':
            count = validator.clear_whitelist()
            print(f"{Colors.GREEN}🧹 Cleared {count} domains from whitelist{Colors.RESET}")

    elif args.command == 'batch':
        try:
            print_banner()
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()

            emails = parse_email_input(content)
            print(f"📁 Loaded {len(emails)} emails from {args.file}")

            results = validator.batch_validate(emails, strict=args.strict)
            print_results(results)

            if args.export:
                exported_file = validator.export_results(results, args.export)
                if exported_file:
                    print(f"\n{Colors.GREEN}📄 Results exported to: {exported_file}{Colors.RESET}")

        except FileNotFoundError:
            print(f"{Colors.RED}❌ File '{args.file}' not found{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error processing file: {e}{Colors.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Validation cancelled by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}💥 Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)