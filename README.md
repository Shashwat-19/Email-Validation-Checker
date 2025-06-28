# 📧 Email-Validation-Checker

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Regex](https://img.shields.io/badge/Regex-Validated-critical?logo=regex)
![CLI](https://img.shields.io/badge/Interface-Command%20Line-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-blue)

## 🚀 Overview

The **Email-Validation-Checker** is a Python CLI utility to validate email addresses using regex and a domain whitelist. It supports batch validation, live domain management (add/remove/list), and helps in cleaning datasets or verifying user inputs efficiently.

🔹 **Use Cases**:
- Cleaning CSV/email lists before import  
- Validating form inputs or user entries  
- Whitelisting corporate/personal domains  

🔹 **Target Audience**:
- Backend developers, data engineers, QA testers, data analysts

---

## 🎯 Key Features

- ✅ Regex-based format validation  
- ✅ Domain whitelist with add/remove support  
- ✅ Batch input via comma/space/semicolon  
- ✅ CLI commands for domain control  
- ✅ Friendly error messages and color-coded output  
- ✅ Designed for extensibility  

---

## 🛠️ Tech Stack & Tools

- **Language**: Python 3.10+
- **Libraries**: `re`, `sys`, `typing`
- **Interface**: Command-Line Based
- **Tested On**: macOS, Linux, Windows (via Terminal/Command Prompt)

---

## 📦 Installation & Setup

### 🔧 Prerequisites

- Python 3.10 or above
- Terminal or command prompt access

### 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Shashwat-19/email-validator.git

# Navigate to the project directory
cd email-validator

# Run the tool
python3 email_validator.py
```
## 📚 Usage Guide

Once started, type any of the following commands:
```
Enter command or emails:
help or ? — Show command help
domains — List allowed domains
add example.com — Add a domain
remove example.com — Remove a domain
exit or quit — Exit the program
```
Paste emails separated by comma, space, or semicolon to validate them


### 🏗️ Project Structure
```
email-validator/
├── .gitignore
├── Code of conduct.md
├── main.py        
├── README.md                 
└── LICENSE                                
```
## Manual Testing Suggestions:

- Run the tool and enter valid/invalid emails
- Test domain add/remove functionality
- Try mixed-case domains and emails
- Validate an empty string or malformed input

### ⚡ Performance Considerations

- Uses compiled regex for faster matching
- Handles large batch inputs with minimal latency
- Designed to avoid crash on malformed inputs


## 🤝 Contribution Guidelines
```
# Fork the repository
# Create a new branch: git checkout -b feature-name
# Make your changes and commit: git commit -m "Added new feature"
# Push to GitHub: git push origin feature-name
# Submit a pull request
```

## 🖥️ Platform Compatibility

- ✅ Windows
- ✅ macOS
- ✅ Linux



