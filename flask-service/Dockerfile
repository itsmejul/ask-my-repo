
FROM continuumio/miniconda3
#ENV PATH="/home/devuser/.local/bin:${PATH}"
# Copy environment file
COPY env.yml /tmp/env.yml

# Create conda environment
RUN conda env create -f /tmp/env.yml
#RUN pip install celery
# Set environment variables
ENV PATH /opt/conda/envs/ask-my-repo-env/bin:$PATH



# Activate environment by default
SHELL ["conda", "run", "-n", "ask-my-repo-env", "/bin/bash", "-c"]

# Set working directory
WORKDIR /app
COPY . .

# Optional: Set entrypoint
# ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "your_script.py"]
CMD ["python", "backend.py"]