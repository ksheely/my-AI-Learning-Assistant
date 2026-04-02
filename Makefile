.PHONY: setup install run 

setup:
	@echo "🛠️  FastAPI Project Setup"
	@python --version
	@python -m venv .venv
	@pip install -r requirements.txt
	@echo "✅ Setup complete!"

install:
	@echo "🔧 Installing Python dependencies..."
	@pip install -r requirements.txt
	@echo "✅ Dependencies installed successfully!"

run:
	@echo "🚀 Starting FastAPI development server..."
	@echo "📍 http://127.0.0.1:8000"
	@echo "📚 API Docs: http://127.0.0.1:8000/docs"
	@echo ""
	uvicorn main:app --host 127.0.0.1 --port 8000 --reload