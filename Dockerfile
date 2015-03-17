FROM python:3.4-onbuild
CMD ["gunicorn", "--config=gunicorn.py", "application.views:app"]
