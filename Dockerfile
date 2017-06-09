FROM yadage/yadage:git-master
RUN pip install matplotlib numpy scipy
RUN pip install ipython==5.4.1 jupyter redis celery 
RUN yum install -y tkinter
RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension
ENV PYTHONPATH /notebook

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents
# kernel crashes.
ENV TINI_VERSION v0.13.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

ADD . /notebook
WORKDIR /notebook

RUN cd workflows/localflow && pip install -e .

RUN cd scikit-optimize && pip install -r requirements.txt && pip install -e .
RUN pip install -U packtivity
RUN pip install -r requirements.txt
RUN mkdir -p ~/.jupyter; printf  "import os\nc.NotebookApp.token = os.environ['THEJUPYTERTOKEN']\n" >> ~/.jupyter/jupyter_notebook_config.py

EXPOSE 8888
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
