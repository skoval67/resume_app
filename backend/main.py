import logging
import subprocess
from time import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from database import engine, Base
from routers.auth import router as auth_router
from routers.resumes import router as resume_router
from config import settings


logger = logging.getLogger("resume_app")
logging.basicConfig(level=logging.INFO)


class ResumeApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.ENV == "DEV":
            # В dev создаём таблицы автоматически
            Base.metadata.create_all(bind=engine)
        elif settings.ENV == "PROD":
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            if not tables:
                logging.info("No tables found — creating schema...")
                Base.metadata.create_all(bind=engine)

            # Прогоняем alembic миграции
            logging.info("Running migrations...")
            try:
                subprocess.run(
                    ["alembic", "upgrade", "head"],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                logging.info("Migrations applied successfully")
            except subprocess.CalledProcessError as e:
                logging.error(f"Migration failed: {e.stderr}")
                raise

        # Служебный маршрут
        @self.get("/status")
        async def status():
            return {"status": "ok"}

        self.include_router(auth_router)
        self.include_router(resume_router)

        # CORS
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Middleware для логирования всех запросов
        @self.middleware("http")
        async def log_requests(request: Request, call_next):
            start_time = time()
            response = await call_next(request)
            process_time = (time() - start_time) * 1000
            logger.info(
                f"{request.method} {request.url.path} "
                f"status={response.status_code} time={process_time:.2f}ms"
            )
            return response


app = ResumeApp(title="Resume API", version="1.0.0", description="API для работы с резюме", root_path="/api")
