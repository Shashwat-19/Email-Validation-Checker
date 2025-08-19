# Email Validation Checker 📧✅

## 🚀 Overview
The **Email-Validation-Checker** is a Python CLI utility to validate email addresses using regex and a domain whitelist. It supports batch validation, live domain management (add/remove/list), and helps in cleaning datasets or verifying user inputs efficiently.

### 🔹 Use Cases:
* **Data Cleaning**: Validate CSV/email lists before database import
* **Form Validation**: Backend verification for user registration forms  
* **Corporate Filtering**: Whitelist company/approved domains only
* **QA Testing**: Bulk test email inputs for applications

### 🔹 Target Audience:
* Backend developers working with user authentication
* Data engineers cleaning email datasets
* QA testers validating form inputs
* Data analysts processing user lists

---

## 🎯 Key Features

| Feature | Description | CLI Command |
|---------|-------------|-------------|
| ✅ **Format Validation** | Regex-based email pattern matching | `validate "email@domain.com"` |
| ✅ **Domain Whitelist** | Add/remove approved domains | `domain add/remove/list` |
| ✅ **Batch Processing** | Process multiple emails at once | `batch emails.txt` |
| ✅ **Strict Mode** | Enhanced validation patterns | `--strict` flag |
| ✅ **Export Results** | Save results to CSV for analysis | `--export results.csv` |
| ✅ **Color Output** | Terminal-friendly colored results | Built-in |

---

## 🛠️ Tech Stack & Requirements

### **Core Stack**
* **Language**: Python 3.10+
* **Libraries**: `re`, `json`, `csv`, `argparse`, `pathlib`
* **Interface**: Command-Line Interface
* **Storage**: JSON-based domain whitelist

### **System Requirements**
```bash
Python 3.10+ (tested on 3.10, 3.11, 3.12)
Terminal/Command Prompt access
No external dependencies required
```

---

## 📦 Installation & Setup

### **Quick Setup**
```bash
# 1. Save the email_validator.py file
# 2. Make it executable (Linux/Mac)
chmod +x email_validator.py

# 3. Test installation
python email_validator.py --help
```

### **Optional: Add to PATH**
```bash
# Linux/Mac - Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:/path/to/email-validator"
alias emailcheck="python /path/to/email_validator.py"

# Windows - Add to system PATH or create batch file
# emailcheck.bat:
@echo off
python "C:\path\to\email_validator.py" %*
```

---

## 🚀 Usage Examples

### **1. Single Email Validation**
```bash
# Basic validation
python email_validator.py validate "john.doe@company.com"

# Strict validation (more restrictive patterns)
python email_validator.py validate "test@domain.co.uk" --strict
```

### **2. Multiple Emails (Comma-separated)**
```bash
# Validate multiple emails
python email_validator.py validate "user1@test.com,user2@demo.org,invalid.email"

# With export to CSV
python email_validator.py validate "john@corp.com,jane@startup.io" --export validation_results.csv
```

### **3. Domain Whitelist Management**
```bash
# Add approved domains
python email_validator.py domain add "company.com"
python email_validator.py domain add "partner.org"

# List all whitelisted domains  
python email_validator.py domain list

# Remove domain
python email_validator.py domain remove "old-domain.com"

# Clear all domains (allows all domains)
python email_validator.py domain clear
```

### **4. Batch File Processing**
```bash
# Create emails.txt with one email per line:
# john@example.com
# jane@test.org  
# invalid.email.format
# admin@company.co.uk

# Process the file
python email_validator.py batch emails.txt

# With strict mode and export
python email_validator.py batch emails.txt --strict --export batch_results.csv
```

---

## 📊 Output Examples

### **Validation Results Display**
```
╔══════════════════════════════════════════════════════════════╗
║                    Email Validation Checker                 ║
║                         Version 1.0.0                       ║
╚══════════════════════════════════════════════════════════════╝

📊 Validation Summary
==================================================
Total Emails:     5
Valid Emails:     3
Invalid Emails:   2  
Success Rate:     60.0%

✅ Valid Emails:
  • john.doe@company.com
  • jane@startup.io
  • admin@corp.co.uk

❌ Invalid Emails:
  • invalid.email - Invalid email format
  • test@blocked.com - Domain 'blocked.com' not in whitelist
```

### **Domain Management**
```bash
$ python email_validator.py domain list

📋 Whitelisted Domains (3)
========================================
 1. company.com
 2. corp.co.uk  
 3. startup.io
```

---

## 🔧 Advanced Configuration

### **Email Validation Patterns**

The tool uses two validation modes:

**Standard Mode** (Default):
```python
r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
```

**Strict Mode** (`--strict` flag):
```python  
r'^[a-zA-Z0-9](?:[a-zA-Z0-9._-]*[a-zA-Z0-9])?@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)*$'
```

### **Whitelist File Structure**
The `domain_whitelist.json` file stores approved domains:
```json
{
  "domains": [
    "company.com",
    "partner.org",
    "client.co.uk"
  ],
  "last_updated": "2024-01-15T10:30:00",
  "total_domains": 3
}
```

### **CSV Export Format**
```csv
Email,Status,Reason,Timestamp
john@company.com,Valid,Valid email,2024-01-15T10:30:15
invalid.format,Invalid,Invalid email format,2024-01-15T10:30:15
test@blocked.com,Invalid,Domain 'blocked.com' not in whitelist,2024-01-15T10:30:15
```

---

## 🔌 Integration Examples

### **1. MERN Stack Integration**
```javascript
// Node.js backend validation
const { spawn } = require('child_process');

function validateEmail(email) {
  return new Promise((resolve, reject) => {
    const validator = spawn('python', ['email_validator.py', 'validate', email]);
    
    let output = '';
    validator.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    validator.on('close', (code) => {
      const isValid = code === 0 && output.includes('Valid email');
      resolve({ email, valid: isValid });
    });
  });
}

// Usage in Express route
app.post('/register', async (req, res) => {
  const { email } = req.body;
  const validation = await validateEmail(email);
  
  if (!validation.valid) {
    return res.status(400).json({ error: 'Invalid email address' });
  }
  
  // Continue with registration...
});
```

### **2. Python/Flask Integration** 
```python
from email_validator import EmailValidator

# Initialize validator
validator = EmailValidator()

# Flask route
@app.route('/validate-email', methods=['POST'])
def validate_email():
    email = request.json.get('email')
    is_valid, reason = validator.validate_email(email)
    
    return {
        'email': email,
        'valid': is_valid,
        'reason': reason
    }
```

### **3. Data Processing Pipeline**
```python
# Process CSV with email column
import pandas as pd

def clean_email_dataset(csv_file):
    df = pd.read_csv(csv_file)
    validator = EmailValidator()
    
    # Add validation columns
    df['email_valid'] = df['email'].apply(
        lambda x: validator.validate_email(x)[0]
    )
    df['validation_reason'] = df['email'].apply(
        lambda x: validator.validate_email(x)[1]
    )
    
    # Filter valid emails only
    clean_df = df[df['email_valid'] == True]
    clean_df.to_csv('cleaned_emails.csv', index=False)
    
    return clean_df
```

---

## 🧪 Testing & Development

### **Unit Tests**
```python
# test_validator.py
import unittest
from email_validator import EmailValidator

class TestEmailValidator(unittest.TestCase):
    def setUp(self):
        self.validator = EmailValidator()
    
    def test_valid_email_format(self):
        self.assertTrue(self.validator.validate_format("test@example.com"))
    
    def test_invalid_email_format(self):
        self.assertFalse(self.validator.validate_format("invalid.email"))
    
    def test_domain_whitelist(self):
        self.validator.add_domain("approved.com")
        self.assertTrue(self.validator.validate_domain("user@approved.com"))

if __name__ == '__main__':
    unittest.main()
```

### **Performance Benchmarks**
```python
# benchmark.py - Test with large datasets
import time
from email_validator import EmailValidator

def benchmark_validation(email_count=10000):
    validator = EmailValidator()
    emails = [f"user{i}@test{i%100}.com" for i in range(email_count)]
    
    start_time = time.time()
    results = validator.batch_validate(emails)
    end_time = time.time()
    
    print(f"Validated {email_count} emails in {end_time - start_time:.2f}s")
    print(f"Rate: {email_count / (end_time - start_time):.0f} emails/second")

benchmark_validation()
```

---

## 🚦 Production Considerations

### **For High-Volume Applications**
* **Caching**: Cache domain validation results
* **Async Processing**: Use threading for batch operations  
* **Rate Limiting**: Implement API rate limits
* **Logging**: Add structured logging for debugging

### **Security Best Practices**
* **Input Sanitization**: Validate input lengths and characters
* **File Permissions**: Secure whitelist file access (600 permissions)
* **DoS Prevention**: Limit batch processing size
* **Audit Trail**: Log all domain whitelist changes

### **Monitoring & Alerts**
```python
# Add to production code
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_validator.log'),
        logging.StreamHandler()
    ]
)

# Log validation events
logger.info(f"Validated {len(emails)} emails, {valid_count} valid")
```

---

## 🔄 Future Enhancements

### **Roadmap Ideas**
* 🌐 **DNS Validation**: Check if domain exists via DNS lookup
* 📧 **SMTP Verification**: Test actual email deliverability  
* 🔌 **API Mode**: HTTP REST API for microservices
* 📊 **Analytics Dashboard**: Web UI for validation statistics
* 🔄 **Auto-sync**: Import domains from corporate directories
* 🚀 **Performance**: Multi-threading for large batches

### **Integration Opportunities**
* **Docker**: Containerized deployment
* **Firebase Functions**: Serverless email validation
* **AWS Lambda**: Cloud-based processing
* **Streamlit**: Web interface for non-technical users

---

## 💡 Troubleshooting

### **Common Issues**

**Issue**: `Permission denied` when saving whitelist
**Solution**: Check file permissions and directory write access
```bash
chmod 755 /path/to/directory
chmod 644 domain_whitelist.json
```

**Issue**: Colors not showing in Windows Terminal
**Solution**: Enable ANSI color support or use modern terminal (Windows Terminal, PowerShell 7+)

**Issue**: Large file processing is slow  
**Solution**: Use batch processing or implement threading
```python
# For large files, process in chunks
def process_large_file(filename, chunk_size=1000):
    with open(filename, 'r') as f:
        emails = []
        for line in f:
            emails.append(line.strip())
            if len(emails) >= chunk_size:
                yield emails
                emails = []
        if emails:
            yield emails
```

---

## 📞 Support & Contributing

### **Getting Help**
* Check existing GitHub issues
* Review troubleshooting section
* Provide sample data when reporting bugs

### **Contributing**
* Fork the repository
* Create feature branches
* Add unit tests for new features
* Follow Python PEP 8 style guidelines
* Submit pull requests with clear descriptions

---

## 📚 Documentation

Comprehensive documentation for this project is available on [Hashnode](https://hashnode.com/@Shashwat56).

> At present, this README serves as the primary source of documentation.

## 📜 License

This project is distributed under the MIT License.  
For detailed licensing information, please refer to the [LICENSE](./LICENSE) file included in this repository.


## 📩 Contact  
### Shashwat  
**Python & Java Developer | Cloud & NoSQL Enthusiast**  

- **Python & Java Development** – Automation, Backend Systems, APIs, and OOP  
- **Cloud & NoSQL** – Docker, AWS, MongoDB, Firebase Firestore  
- **UI/UX Design** – Creating user-focused, scalable, and visually engaging applications  

---

## 🚀 Open Source | Tech Innovation  
Passionate about creating robust applications and leveraging cloud technologies for high-performance solutions.


### 📌 Find me here:  
[<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />](https://github.com/Shashwat-19)  [<img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />](https://www.linkedin.com/in/shashwatk1956/)  [<img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" />](mailto:shashwat1956@gmail.com)  [<img src="https://img.shields.io/badge/Hashnode-2962FF?style=for-the-badge&logo=hashnode&logoColor=white" />](https://hashnode.com/@Shashwat56)
[<img src="https://img.shields.io/badge/HackerRank-15%2B-2EC866?style=for-the-badge&logo=HackerRank&logoColor=white" />](https://www.hackerrank.com/profile/shashwat1956)

Feel free to connect for tech collaborations, open-source contributions, or brainstorming innovative solutions!


**Built for developers who need reliable email validation in their data pipelines and applications! 🚀**