import os
import sys
import subprocess

# Inject newly generated directory into Python scope
sys.path.append(os.getcwd())
import settings
import logging


logger = logging.getLogger(__name__)

logger.info(f'RAUSYS XGS Tanker cookiecutter generation completed; Output Path is {os.getcwd()}')


{% if cookiecutter.run_requirements %}
try:
	logger.info('Auto-installing Python dependencies...')
	path = os.path.join(os.getcwd().strip(), 'requirements.txt')
	subprocess.run([sys.executable, "-m", "pip", "install", "-r", path], check=True)
except Exception as e:
	logger.exception(f'Installation failed, please continue manually! {e}')
	exit(0)  # non-zero exit code, so newly generated directory is not deleted again
{% endif %}

{% if cookiecutter.run_instantly %}
try:
	logger.info('Kicking off main XGS tanking process! Switching to richer interface...')
	subprocess.run([sys.executable, "main.py"])
except Exception as e:
	logger.exception(f'XGS Tanker Script failed; please continue manually! {e}')
	exit(0)  # non-zero exit code, so newly generated directory is not deleted again
{% endif %}
