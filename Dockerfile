# FROM sseemayer/graphviz:latest

FROM python:3.9.1-alpine
WORKDIR /usr/src/app
COPY clean_parser clean_parser
COPY plagiarism_checker plagiarism_checker
COPY SyntaClean.py SyntaClean.py
COPY requirements-nogui.txt requirements-nogui.txt
COPY dist dist
RUN pip install -r requirements-nogui.txt