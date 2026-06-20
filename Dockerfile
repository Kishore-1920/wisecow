# Use Ubuntu as base image since wisecow.sh is a bash script
# that needs apt package manager for fortune-mod and cowsay
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages:
# - fortune-mod: generates random fortune cookie messages
# - cowsay: renders the cow ASCII art with the message
# - netcat-openbsd: used by wisecow.sh to serve HTTP responses
# - bash: shell to run the script
RUN apt-get update && apt-get install -y \
    fortune-mod \
    cowsay \
    netcat-openbsd \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add cowsay to PATH (it installs to /usr/games by default on Ubuntu)
ENV PATH="/usr/games:${PATH}"

# Set working directory inside the container
WORKDIR /app

# Copy the wisecow shell script into the container
COPY wisecow.sh .

# Make the script executable
RUN chmod +x wisecow.sh

# Expose the port wisecow listens on (default: 4499)
EXPOSE 4499

# Run wisecow.sh when the container starts
CMD ["bash", "wisecow.sh"]
