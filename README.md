# 📚 Rulebook-QA

A web-based chatbot that helps students find information from university rules and regulations.

Instead of going through multiple documents manually, users can simply ask a question and get the relevant rulebook information along with its source and section.

## 🔗 Live Demo

👉 https://rulebook-qa.vercel.app/

## 📌 About the Project

University rules are usually available across different documents such as attendance policies, examination rules, hostel guidelines, fee details, and scholarship policies.

I built **Rulebook-QA** to make this information easier to search. A user can ask a question in the chatbot, and the system searches the available rulebook content and returns the most relevant information.

The response also shows the **source document, section, similarity score, and retrieved passage** so the user can check where the information came from.

## ✨ Features

- 💬 Ask questions about university rules
- 📄 Search across multiple rulebook documents
- 🔎 Retrieve relevant passages
- 📌 Show source and section references
- 📊 Display similarity scores
- ⚠️ Identify questions that are not covered
- 🔴 Detect conflicting provisions
- 🌐 Simple web-based chatbot interface
- 🚀 Deployed on Vercel

## 🗂️ Documents Used

The project currently uses the following documents:

| Document | Content |
|---|---|
| `academic_regulations.md` | Academic rules and regulations |
| `attendance_policy.md` | Attendance requirements |
| `examination_rules.md` | Examination rules |
| `discipline_policy.md` | Discipline-related rules |
| `hostel_handbook.md` | Hostel regulations |
| `scholarship_policy.md` | Scholarship information |
| `fee_deadlines.csv` | Fee deadlines and late fees |
| `university_regulations.pdf` | General university regulations |

## ⚙️ How It Works

```text
University Documents
        ↓
   Text Extraction
        ↓
    Text Chunking
        ↓
 Similarity-based Search
        ↓
 Relevant Passages
        ↓
 Response / Conflict Check
        ↓
     FastAPI API
        ↓
   Web Chat Interface
