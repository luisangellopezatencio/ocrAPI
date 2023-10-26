FROM challisa/easyocr
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

RUN pip install fastapi
RUN pip install uvicorn
RUN pip install pydantic
RUN pip install python-multipart
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]