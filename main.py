import re
import sys
from typing import Tuple, Set


class EmailValidator:
    """Email validation class with domain whitelist functionality."""
    
    def __init__(self, allowed_domains: Set[str] = None):
        """
        Initialize the email validator.
        
        Args:
            allowed_domains: Set of allowed email domains. Defaults to common providers.
        """
        self.allowed_domains = allowed_domains or {
            'gmail.com', 
            'yahoo.com', 
            'outlook.com',
            'hotmail.com',
            'icloud.com'
        }
        
        # More comprehensive email regex pattern
        self.email_regex = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
    
    def validate_email(self, email: str) -> Tuple[bool, str]:
        """
        Validate a single email address.
        
        Args:
            email: Email address to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not email or not isinstance(email, str):
            return False, "Empty or invalid input"
        
        email = email.strip().lower()
        
        # Check email format
        if not self.email_regex.match(email):
            return False, "Invalid email format"
        
        # Extract domain
        try:
            domain = email.split('@')[1]
        except IndexError:
            return False, "Invalid email format"
        
        # Check if domain is allowed
        if domain not in self.allowed_domains:
            return False, f"Domain '{domain}' not allowed"
        
        return True, domain
    
    def validate_batch(self, emails: str) -> list:
        """
        Validate multiple email addresses from a string.
        
        Args:
            emails: String containing comma or space separated emails
            
        Returns:
            List of tuples (email, is_valid, message)
        """
        results = []
        
        # Split by comma, semicolon, or whitespace
        email_list = re.split(r'[,;\s]+', emails.strip())
        
        for email in email_list:
            email = email.strip()
            if not email:
                continue
                
            valid, message = self.validate_email(email)
            results.append((email, valid, message))
        
        return results
    
    def add_domain(self, domain: str) -> None:
        """Add a domain to the allowed list."""
        self.allowed_domains.add(domain.lower())
    
    def remove_domain(self, domain: str) -> None:
        """Remove a domain from the allowed list."""
        self.allowed_domains.discard(domain.lower())
    
    def list_domains(self) -> Set[str]:
        """Get the current list of allowed domains."""
        return self.allowed_domains.copy()


def print_results(results: list) -> None:
    """Print validation results in a formatted way."""
    if not results:
        print("No valid emails found to process.")
        return
    
    print("\nValidation Results:")
    print("-" * 50)
    
    for email, valid, message in results:
        status = "✓" if valid else "✗"
        if valid:
            print(f"{status} {email:<30} Valid ({message})")
        else:
            print(f"{status} {email:<30} {message}")


def print_help() -> None:
    """Print help information."""
    help_text = """
Email Validator Commands:
- Enter email addresses (comma or space separated)
- 'help' or '?' - Show this help
- 'domains' - List allowed domains
- 'add <domain>' - Add a domain to allowed list
- 'remove <domain>' - Remove a domain from allowed list
- 'exit' or 'quit' - Exit the program
    """
    print(help_text)


def main():
    """Main application loop."""
    validator = EmailValidator()
    
    print("Email Validator Tool")
    print("=" * 40)
    print(f"Allowed domains: {', '.join(sorted(validator.list_domains()))}")
    print("Type 'help' for commands or 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("Enter command or emails: ").strip()
            
            if not user_input:
                continue
            
            # Handle exit commands
            if user_input.lower() in ('exit', 'quit'):
                print("Goodbye!")
                break
            
            # Handle help command
            elif user_input.lower() in ('help', '?'):
                print_help()
                continue
            
            # Handle domains list command
            elif user_input.lower() == 'domains':
                domains = sorted(validator.list_domains())
                print(f"\nAllowed domains ({len(domains)}):")
                for domain in domains:
                    print(f"  • {domain}")
                continue
            
            # Handle add domain command
            elif user_input.lower().startswith('add '):
                domain = user_input[4:].strip()
                if domain:
                    validator.add_domain(domain)
                    print(f"Added domain: {domain}")
                else:
                    print("Please specify a domain to add")
                continue
            
            # Handle remove domain command
            elif user_input.lower().startswith('remove '):
                domain = user_input[7:].strip()
                if domain:
                    if domain.lower() in validator.list_domains():
                        validator.remove_domain(domain)
                        print(f"Removed domain: {domain}")
                    else:
                        print(f"Domain '{domain}' not found in allowed list")
                else:
                    print("Please specify a domain to remove")
                continue
            
            # Validate emails
            results = validator.validate_batch(user_input)
            print_results(results)
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()