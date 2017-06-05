FROM yadage/yadage:git-master
RUN pip install matplotlib numpy scipy
RUN pip install ipython==5.4.1 jupyter redis celery
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

EXPOSE 8888
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
