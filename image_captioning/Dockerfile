FROM python:2.7-slim

WORKDIR /app
COPY ./requirements.txt /app

# Install Bazel
RUN apt-get update
RUN apt-get install -y gnupg2 curl
RUN curl https://bazel.build/bazel-release.pub.gpg | apt-key add - 
RUN echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list

# Install Python Packages
RUN pip install -r requirements.txt

# Install NLTK punkt data
RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt