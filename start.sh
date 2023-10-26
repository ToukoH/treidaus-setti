SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd "$SCRIPT_DIR" || { echo "Script directory not found"; exit 1; }

if [ ! -d ".venv" ]; then
  echo ".venv directory not found"
  exit 1
fi

npm start &

source .venv/bin/activate
uvicorn server.data_pipeline.data_pipeline:app --reload &

wait
