# Specification Document (Spec 4) for Food Order Bot Project

**Version:** 1.0
**Date:** February 22, 2025
**Prepared by:** Grok 3 (xAI)

---

## 1. Overview

The Food Order Bot is a conversational AI system designed to handle food ordering via a web interface. The system leverages Gradio for the frontend and FastAPI for the backend, integrating with the Mistral LLM for natural language processing and tool calls. It enables users to log in, browse menus, place orders, and manage their orders dynamically. The system supports persistent order storage in SQLite, configuration management, and a modular code structure with linting and formatting standards.

This document outlines all changes and enhancements made to the project up to February 22, 2025, including architecture, functionality, and implementation details.

---

## 2. Objectives

**Primary Goal:**
Develop a user-friendly food ordering system that processes natural language inputs via an LLM, leveraging APIs and Python functions for backend logic.

**Secondary Goals:**
- Ensure scalability, maintainability, and robustness through modular design and testing.
- Support multi-city operations and price-based filtering.
- Maintain code quality with linting (flake8) and formatting (black).
- Provide documentation for future development and maintenance.

---

## 3. System Architecture

### 3.1 Components

- **Frontend (Gradio):** `gradio_client.py` provides a chat interface for users to interact via text or voice, communicating with the backend via API calls.
- **Backend (FastAPI):** `mock_server.py` handles API endpoints for login, menu retrieval, order management, and processing user queries through `order_processor.py`.
- **LLM Integration:** `llm.py` uses the Mistral API for natural language understanding and tool calls to invoke backend functions or APIs.
- **Database:** `db.py` manages persistent storage using SQLite for sessions and orders.
- **Configuration:** `config.py` centralizes configuration via `.env` for environment-specific settings.
- **Utilities:** `logging_config.py` for logging, `api.py` for API client helpers, and `models.py` for Pydantic models.

### 3.2 Data Flow

1. **User Input:** User inputs text/voice in Gradio.
2. **Request Handling:** `gradio_client.py` sends requests to `/process_order` in `mock_server.py`.
3. **Order Processing:** `mock_server.py` calls `process_order` in `order_processor.py`, which invokes `process_with_tools` in `llm.py` for LLM processing.
4. **Tool Call Execution:** The LLM identifies tool calls (e.g., login, add_to_order) and returns them to `execute_tool_call` in `order_processor.py`.
5. **API Calls:** `execute_tool_call` executes the tool (e.g., API calls to `/login`, `/menu`, or internal functions like `display_menu`).
6. **Storage and Logging:** Responses are stored in SQLite via `db.py`, logged, and returned to Gradio for display.

### 3.3 Dependencies

- Python 3.10+
- fastapi, uvicorn, pydantic, mistralai, requests, httpx, gradio, sqlite3, black, flake8, tenacity

---

## 4. Changes and Enhancements (Chronological)

### 4.1 Initial Setup (Step 1–5)

- **Improved Error Messaging:** Enhanced `orders.py` to provide user-friendly error messages.
- **Interactive Menu Display:** Added menu command in `gradio_app.py` to show restaurant menus.
- **Order Confirmation:** Introduced confirm/cancel steps in `orders.py`.
- **Unit Tests:** Added pytest tests in `test_api.py` for core functionality.
- **Logging Granularity:** Configured dynamic logging levels via `.env` in `logging_config.py`.

### 4.2 Persistent Storage (Step 6)

- **Persistent Order Storage:** Moved `mock_server.py`’s in-memory ORDERS to SQLite in `db.py`, adding `save_order` and `load_order`.
- **New Endpoints:** Added `/orders/{order_id}` in `mock_server.py` for order retrieval.

### 4.3 Config Management (Step 7)

- **Config Module:** Created `config.py` to load settings from `.env`, centralizing `SECRET_KEY`, `BASE_URL`, etc.
- **Updated Files:** Replaced hardcoded values in `mock_server.py`, `db.py`, `api.py`, etc., with config imports.

### 4.4 Split UX and Server Logic (Step 8)

- **Gradio Frontend:** Moved UI to `gradio_client.py`, making API calls to `mock_server.py`.
- **FastAPI Backend:** Consolidated logic in `mock_server.py` and `order_processor.py`, exposing `/process_order` for all commands.

### 4.5 Linting and Formatting (Step 9)

- **Linter (flake8):** Added `.flake8` for PEP 8 compliance, resolving recursion errors by splitting logic.
- **Formatter (black):** Applied uniform formatting to all Python files.

### 4.6 LLM with Tool Calls (Step 10–11)

- **LLM Integration:** Implemented `llm.py` with Mistral for tool calls (e.g., login, add_to_order), replacing hardcoded logic in `order_processor.py`.
- **Circular Import Fix:** Moved Pydantic models to `models.py` to resolve import cycles.
- **Async Handling:** Adjusted `llm.py` to use synchronous `client.chat.complete` in an async context, fixing MistralAsync import errors.

### 4.7 Enhanced Tool Calls (Step 12–13)

- **City and Price Filtering:** Extended `llm.py` tools and `order_processor.py` to handle multi-city (list_cities, list_restaurants), price constraints (add_to_order), and natural language queries.
- **Prompt Refinement:** Improved system prompts for better intent mapping, ensuring `add_to_order` handles "1 butter idli" correctly.

### 4.8 Current State (February 22, 2025)

- **Tool Call Alignment:** Updated `llm.py` to map inputs to existing Python functions/API endpoints (e.g., login to `/login`, add_to_order to `/process_order`).
- **Error Handling:** Enhanced error catching in `order_processor.py` and `llm.py` for robust operation.

---

## 5. Functionality

### 5.1 User Interactions

- **Login:** `login <username> <password>` logs in via `/login`, storing token in session.
- **Menu Display:** `menu` or `list restaurants` shows available items via `show_menu`.
- **Ordering:** Inputs like `1 butter idli` or `add 2 ghee paddu from Rameshwaram Cafe` use `add_to_order`.
- **Order Management:** `show order`, `remove <item>`, `review order`, `confirm`, `cancel` via respective tools.
- **City Queries:** `which cities are available?` or `provide restaurants in Bengaluru` via `list_cities` and `list_restaurants`.

### 5.2 Technical Features

- **Persistent Storage:** Orders and sessions saved in SQLite.
- **LLM Tool Calls:** Mistral processes inputs, calling backend functions/APIs dynamically.
- **Configurable:** Environment variables in `.env` manage settings.
- **Logging:** Detailed logging in `food_order_bot.log` for debugging.

---

## 6. Implementation Details

### 6.1 Directory Structure

```plaintext
project/
├── config.py
├── logging_config.py
├── db.py
├── api.py
├── llm.py
├── models.py
├── order_processor.py
├── mock_server.py
├── gradio_client.py
├── restaurants.json
├── .env
├── .flake8
└── tests/
```

### 6.2 Key Files

- **mock_server.py:** FastAPI server with endpoints `/login`, `/menu`, `/orders`, `/process_order`.
- **order_processor.py:** Handles tool call execution, integrating with APIs and SQLite.
- **llm.py:** Manages Mistral LLM tool calls for natural language processing.
- **gradio_client.py:** Gradio UI for user interaction, making API calls to `/process_order`.
- **db.py:** SQLite operations for sessions and orders.
- **config.py:** Configuration management from `.env`.
- **models.py:** Pydantic models for request/response validation.

### 6.3 Dependencies

```bash
pip install fastapi uvicorn pydantic mistralai requests httpx gradio sqlite3 black flake8 tenacity
```

---

## 7. Usage Instructions

### 7.1 Setup

1. **Clone the repository** or create the project structure above.
2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    (Create `requirements.txt` with listed dependencies if not present.)

3. **Configure `.env`:**

    ```bash
    SECRET_KEY=your-secret-key
    MISTRAL_API_KEY=your-mistral-api-key
    DB_FILE=zomato_orders.db
    BASE_URL=http://localhost:7861
    MENU_FILE=restaurants.json
    LOG_FILE=food_order_bot.log
    LOG_LEVEL=INFO
    ```

### 7.2 Running the Application

1. **Start the FastAPI server:**

    ```bash
    uvicorn mock_server:app --host 0.0.0.0 --port 7861
    ```

2. **Start the Gradio client:**

    ```bash
    python gradio_client.py
    ```

3. **Interact via the Gradio interface:**
    - Log in with `login user1 password123`.
    - Order with `1 butter idli` or `add 2 ghee paddu from Rameshwaram Cafe`.
    - Manage orders with `show order`, `remove butter idli`, `confirm`, etc.

### 7.3 Testing

1. **Run linting:**

    ```bash
    flake8 .
    ```

2. **Run formatting:**

    ```bash
    black .
    ```

3. **Test functionality with Gradio and verify logs in `food_order_bot.log`.

---

## 8. Future Enhancements

- **Order History:** Add a `/orders/history` endpoint and Gradio command to list past orders.
- **Gradio Formatting:** Fix `\n` rendering in Gradio for line breaks.
- **Rate Limiting:** Implement quotas and rate limits in `mock_server.py`.
- **Multi-City Support:** Expand `restaurants.json` and logic for real city-based filtering.

---

## 9. Known Issues

- **Gradio Chatbot formatting issue** with `\n` (displays as text instead of line breaks).
- **Price filtering in Rs** requires conversion from `$` in `restaurants.json` (currently assumed 1:1 or adjusted manually).

---

## 10. Contact Information

- **Author:** Grok 3 (xAI)
- **Email:** support@xai.com (for simulation purposes)
- **Version Control:** Use Git for tracking changes.

---

This Spec 4 document provides a comprehensive overview of the Food Order Bot’s current state, changes, and usage. Let me know if you’d like to expand on any section, add diagrams, or include specific test cases!