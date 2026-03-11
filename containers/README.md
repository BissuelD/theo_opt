# Containers

This directory contains everything needed to build and run containerized versions of the interactive figures using either [Apptainer](https://apptainer.org/) or [Docker](https://www.docker.com/).

## How it works

The build workflow is split into two stages:

### 1. Guix package build

[GNU Guix](https://guix.gnu.org/) is used as the foundation. It produces a fully reproducible environment by installing all required Python packages and LaTeX tools declared in [`guix/theo_opt_lectures-manifest.scm`](guix/theo_opt_lectures-manifest.scm). The exact Guix revision is pinned in [`guix/channels.scm`](guix/channels.scm), guaranteeing bit-for-bit reproducibility regardless of when the build is run.

Depending on the target runtime, Guix outputs either:

- a **SquashFS archive** (for Apptainer), or
- a **Docker archive** (for Docker/OCI).

### 2. Container image build

The container image is then assembled on top of the Guix-produced archive:

- **Apptainer**: the SquashFS archive is referenced in [`def-files/from-guix-definition.def`](def-files/from-guix-definition.def) as the base layer. The definition file copies the project source files into `/opt/theo_opt/`, rewrites relative paths to absolute ones, and sets `launcher.py` as the default runscript.
- **Docker**: the Docker archive is loaded into the local Docker daemon. The `FROM` line of [`Dockerfile`](Dockerfile) is updated to reference this base image. The `Dockerfile` then copies the project source files, rewrites paths, and sets `launcher.py` as the default command. [`docker-compose.yml`](docker-compose.yml) handles X11 display forwarding so the GUI works on the host.

---

## Installing the required tools

| Tool               | Installation guide                                                                                                   |
|--------------------|----------------------------------------------------------------------------------------------------------------------|
| **GNU Guix**       | [Official guide](https://guix.gnu.org/manual/en/html_node/Installation.html)                                         |
|                    | or [Diamond's guide](https://diamond-diadem.github.io/documentation/install/install-guix/)                           |
| **Apptainer**      | [Official guide](https://apptainer.org/docs/admin/main/installation.html)                                            |
|                    | or [DIAMOND's guide with video tutorials](https://diamond-diadem.github.io/documentation/install/install-apptainer/) |
| **Docker Engine**  | [Docker installation guide](https://docs.docker.com/engine/install/)                                                 |
| **Docker Compose** | Included with Docker Desktop, or see [installation guide](https://docs.docker.com/compose/install/)                  |

> **Note:** Guix must be installed on the build host for both workflows. Apptainer and Docker are only needed for their respective workflow.

---

## Using the build scripts

Both scripts must be run from within the `containers/` directory.

### `build-apptainer-from-guix.sh`

Builds the Apptainer image `images/theo_opt_interactive.sif`.

```bash
cd containers/
bash build-apptainer-from-guix.sh
```

**What it does:**

1. Calls `guix time-machine` with [`guix/channels.scm`](guix/channels.scm) to build a SquashFS pack from the manifest.
2. Patches the `From:` line in [`def-files/from-guix-definition.def`](def-files/from-guix-definition.def) with the path to the freshly built SquashFS file.
3. Patches the source paths in the `%files` section of [`def-files/from-guix-definition.def`](def-files/from-guix-definition.def) to match the current repository location automatically.
4. Runs `apptainer build` to produce [`images/theo_opt_interactive.sif`](images/theo_opt_interactive.sif).

**Running the image:**

```bash
# Launch the interactive figures GUI
apptainer run images/theo_opt_interactive.sif

# With explicit display forwarding (should not be needed as Apptainer forwards DISPLAY by default)
apptainer run --env DISPLAY=$DISPLAY images/theo_opt_interactive.sif

# Open an interactive shell inside the container
apptainer shell images/theo_opt_interactive.sif

# Read the full built-in help
apptainer run-help images/theo_opt_interactive.sif
```

---

### `build-docker-from-guix.sh`

Builds the Docker image and optionally starts the container.

```bash
cd containers/

# Build only (update Dockerfile with the new base image)
bash build-docker-from-guix.sh

# Build and immediately start the container via Docker Compose
bash build-docker-from-guix.sh compose
```

**What it does:**

1. Calls `guix time-machine` with [`guix/channels.scm`](guix/channels.scm) to build a Docker archive from the manifest.
2. Loads the archive into the local Docker daemon with `docker load`.
3. Patches the `FROM` line in [`Dockerfile`](Dockerfile) with the name of the newly loaded image.
4. *(With `compose` argument)* Runs `docker compose up` using [`docker-compose.yml`](docker-compose.yml), which builds the final image and starts the container with X11 forwarding enabled.

**Without the `compose` argument**, you can start the container manually afterwards:

```bash
cd containers/
docker compose up
```

## Distribution

The built Apptainer image (`images/theo_opt_interactive.sif`) can be distributed as a single file. The Docker image can be pushed to a registry or saved as a tarball with `docker save`.

It is important to note that the final user only needs the container runtime (Apptainer or Docker) and the images to run the interactive figures. They do not need Guix or any of the build tools, as the container image includes everything needed to run the application.
