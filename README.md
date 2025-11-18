
# 🚀 Case AutoU — Aplicação Flask para Análise e Respostas Automáticas

Este projeto é uma aplicação web desenvolvida em **Python + Flask** para **análise e classificação automática de e-mails**, gerando respostas instantâneas utilizando o **Gemini AI**.  
O frontend usa **HTML** e **JavaScript** integrado com **Tailwind CSS** para uma interface limpa e responsiva.

---

## 🛠 Tecnologias Utilizadas

### **Backend**
- Python  
- Flask  
- Gemini API (para geração automática das respostas)  

### **Frontend**
- HTML  
- JavaScript  
- Tailwind CSS
  
---

## 📦 Como Rodar o Projeto

### **1️⃣ Clonar o repositório**
```bash
git clone https://github.com/Venturaa10/case_AutoU
cd case_AutoU
```

---

### **2️⃣ Criar e ativar o ambiente virtual**

#### **Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

#### **macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

Após ativar, seu terminal deve exibir algo como:
```
(venv) usuario@pc:~/case_AutoU$
```

---

### **3️⃣ Instalar dependências**
```bash
pip install -r requirements.txt
```

---

### **4️⃣ Rodar a aplicação**
Na raiz do projeto:
```bash
python3 run.py
```

Saída esperada:
```
Serving Flask app 'app'
Debug mode: on
Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

---

### **5️⃣ Acessar no navegador**
Abra:

👉 **http://127.0.0.1:5000/**

--- 

### **6️⃣ Configurar a API Key do Gemini**

1. Acesse: [AI Studio](https://aistudio.google.com/)  
2. Faça login com sua conta Google.  
3. No canto inferior esquerdo, clique em **"Get API Key"**.  
4. No canto superior direito, clique em **"Criar chave da API"**.  
5. Dê um nome à chave e selecione **Criar** ou **Importar Projeto**.  
6. Clique no botão de copiar ao lado da informação sobre o "nível da cota", **Copy API Key** para copiá-la.  
7. No arquivo **`.env`** na raiz do projeto, adicione a variável de ambiente:

```env
GEMINI_API_KEY="SUA_CHAVE_AQUI"


Pronto! Aplicação estará configurada e rodando localmente. 🎉

