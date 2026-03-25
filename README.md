# 🤖 AI Lead Catcher & Smart CRM Widget

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

An intelligent, multilingual B2B sales widget built with Python and the OpenAI API. This application acts as an autonomous AI Sales Manager that engages with website visitors, organically collects project details, and saves structured data directly into a CRM database using **OpenAI Function Calling**.

🔗 **[Live Demo](https://YOUR-APP-LINK.streamlit.app/)** *(Replace with your Streamlit Cloud link)*
🔐 **Admin Panel Password:** `admin123` *(Example)*

---

## 🎯 Core Architecture & Magic

Unlike standard chatbots that simply generate text, this agent is deeply integrated with the backend infrastructure:

1. **Contextual Memory:** The AI maintains session state, remembering the user's name and project details throughout the conversation.
2. **Dynamic Function Calling:** Once the AI organically collects 4 mandatory data points (Name, Contact Info, Service, and Budget), it autonomously triggers a hidden Python backend function (`save_lead_to_db`).
3. **Data Normalization:** * **Language Agnostic:** The AI chats in the user's native language (Russian, Spanish, German, etc.) but translates all saved data into English for clean database records.
   * **Smart Currency Conversion:** If a user provides a budget in local currency (e.g., EUR or RUB), the AI calculates the approximate USD equivalent on the fly before saving it to the database.
   * **Contact Resolution:** The AI parses social media handles (e.g., `@username`) and asks the user to clarify the platform (Telegram, Instagram, etc.), saving the `contact_type` accordingly.

## ✨ Key Features

* **Dual-View UI:** A split-screen Streamlit interface featuring a public-facing agency website with a chat widget, and a hidden Admin Panel.
* **Live CRM Dashboard:** Admins can view newly captured leads in real-time.
* **Admin Controls:** Password-protected functionality to view and securely delete mock leads from the SQLite database.
* **Graceful Farewells:** The AI generates a customized, polite goodbye message in the user's exact language immediately after committing data to the backend.

## 🛠️ Tech Stack

* **Frontend & Framework:** Streamlit (Python)
* **AI Provider:** OpenAI API (`gpt-4o-mini` model)
* **Database:** SQLite3
* **Environment Management:** `python-dotenv`

---

## 🚀 Local Setup & Installation

To run this project locally:

**1. Clone the repository**
```bash
git clone [https://github.com/asimerole/Smart-Lead-Router.git](https://github.com/asimerole/Smart-Lead-Router.git)
cd Smart-Lead-Router
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Create a `.env` file in the root directory and add your credentials:
```bash
OPENAI_API_KEY=sk-your-openai-api-key
ADM_PWD=your_admin_password
```

**4. Run the application**
```bash
streamlit run web.py
```
The application will automatically initialize the `orders.db` SQLite database on the first run.

---

Developed as an advanced showcase of AI-driven business automation and prompt engineering.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
