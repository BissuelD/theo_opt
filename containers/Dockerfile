FROM python-python-scipy-python-numpy:latest

WORKDIR /opt/theo_opt

# Equivalent of Apptainer %files.
COPY *.py /opt/theo_opt/
COPY stuff /opt/theo_opt/stuff
COPY man /opt/theo_opt/man
COPY EMpy /opt/theo_opt/EMpy

# Keep this behavior from the Apptainer %post section.
RUN touch /etc/passwd /etc/group

# Rewrite hardcoded relative paths the same way as in the Apptainer definition.
RUN python3 << 'EOF'
import glob
import os

for filepath in glob.glob('/opt/theo_opt/*.py'):
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content.replace('./stuff', '/opt/theo_opt/stuff')

    lines = new_content.splitlines()
    for i, line in enumerate(lines):
        if 'create_launch_button' in line:
            parts = line.split("'")
            for j, part in enumerate(parts):
                if part.endswith('.py'):
                    parts[j] = '/opt/theo_opt/' + part
            lines[i] = "'".join(parts)

        if 'show_manual' in line:
            parts = line.split('"')
            for j, part in enumerate(parts):
                if part.startswith('man'):
                    parts[j] = '/opt/theo_opt/' + part
            lines[i] = '"'.join(parts)

    new_content = '\n'.join(lines)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f'Updated: {filepath}')
    else:
        print(f'No changes: {filepath}')

gui_stuff_path = '/opt/theo_opt/stuff/gui_stuff.py'
if os.path.exists(gui_stuff_path):
    with open(gui_stuff_path, 'r') as f:
        content = f.read()

    new_content = content.replace(
        'text=filename',
        'text=filename.replace("/opt/theo_opt/", "")'
    )

    if new_content != content:
        with open(gui_stuff_path, 'w') as f:
            f.write(new_content)
        print(f'Updated: {gui_stuff_path}')
    else:
        print(f'No changes: {gui_stuff_path}')
EOF

LABEL org.opencontainers.image.title="Theoretical Optics Interactive Figures"
LABEL org.opencontainers.image.description="Supplemental interactive figures for 'Lectures in Theoretical Optics' by Falk Lederer and Stefan Skupin (Springer, 2026)"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Stefan Skupin <stefan.skupin@univ-lyon1.fr>, Falk Lederer <falk.lederer@uni-jena.de>"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/sskupin/theo_opt"
LABEL org.opencontainers.image.url="https://link.springer.com/book/9783662726334"
LABEL maintainer="Dylan Bissuel <dylan.bissuel@univ-lyon1.fr>"

CMD ["python3", "/opt/theo_opt/launcher.py"]
