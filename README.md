# HEIC Converter — Learning Project

A small full-stack app that converts **HEIC** (iPhone / HEIF) images into **PNG** 
Built from scratch to understand *how modern web systems actually work*

---

## What It Does

- Upload a `.HEIC` photo through a simple web interface.  
- The backend decodes the HEIC file using `pillow-heif` and re-encodes it into PNG format.  
- The converted image streams back to the browser as a downloadable file.  

---

## Why I’m Building This

This is my sandbox for learning web app concepts. I can freely brake things and learn through trial and error.
Every part of this project exists to teach me a core engineering concept:

| Goal | What I’m learning |
|------|-------------------|
| **FastAPI backend** | How HTTP requests are parsed, validated, and streamed back to the client. |
| **React frontend** | How browsers handle file uploads, form data, and API responses. |
| **Testing with pytest** | How to write unit tests and integration tests that guarantee correctness. |
| **pillow-heif + Pillow** | How image decoding and encoding actually work at the binary level. |
| **Monorepo structure** | How to organize a real project with clear separation between backend, frontend, and infra. |
| **Hosting & deployment** | How to containerize, set up Nginx as reverse proxy, manage file size limits, and push to the web. |
| **Streaming responses** | Why streaming beats buffering for large files, and how to implement it safely. |
| **Error handling** | How to return meaningful HTTP errors (400/422) without leaking internals. |
| **Version control discipline** | Keeping `.venv`, caches, and build junk out of git. |
| **End-to-end communication** | Seeing how frontend → backend → response all connect through HTTP. |

I’m treating this like a **mini full-stack bootcamp** I designed for myself.

---

## Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — ASGI web framework  
- [pillow-heif](https://pypi.org/project/pillow-heif/) — HEIC/HEIF support for Pillow  
- [Pillow](https://pypi.org/project/Pillow/) — image processing  
- [pytest](https://docs.pytest.org/) — testing framework  
- [uvicorn](https://www.uvicorn.org/) — ASGI server  

**Frontend**
- [React](https://react.dev/) 

**Infra (not implemented yet)**
- Docker + Nginx (later)  
- GitHub Actions or simple CI for testing (planned)  
- Deployed as one container exposing both frontend and backend  

---

## Tests

Everything starts with **tests first**.  
There are two levels:

- **Unit tests** (`backend/tests/test_convert_heic_unit.py`)  
  Validate that the image decoding and conversion logic is bulletproof.  
- **Integration tests** (`backend/tests/test_api_heic.py`)  
  Hit the FastAPI endpoint with real HEIC and JPG files to ensure API correctness.  

