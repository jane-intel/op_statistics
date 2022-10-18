# Statistic collector
`collect.py` script scans particular directory for models with requested expension. It collects operation statistics per each model. Report is provided per operation, per model and in consolidated form.

## Prerequisites
```
pip3 install -r requirements.txt
```

## Usage
```
python3 collect.py path/to/directory extension
```
Extension examples:
- onnx
- xml
