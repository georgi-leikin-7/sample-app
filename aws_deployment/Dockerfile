FROM localstack/localstack-pro:3.7.2


# Remove previous Docker packages
RUN for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do apt-get remove $pkg; done

# Add Docker's official GPG key:
RUN apt-get update
RUN apt-get install -y ca-certificates curl gnupg
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
RUN echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update

# Install docker
RUN apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


# Install CDK and CDK Local
RUN npm install -y -g aws-cdk-local aws-cdk
