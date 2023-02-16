FROM python:3.10.2

RUN apt-get update

EXPOSE 8080

COPY . ./

RUN pip install -r requirements.txt

CMD streamlit run --server.port 8080 dashboard_ppgeec/professors_graph.py