import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_TREE = Path('skill_tree.json')

def load_skill_tree():
    with SKILL_TREE.open('r', encoding='utf-8') as f:
        return json.load(f)

def run_command(cmd):
    # run via shell to support simple pipeline checks; return (exit_code, stdout)
    try:
        proc = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
        return proc.returncode, proc.stdout.strip()
    except Exception as e:
        return 255, str(e)

def expand_template(cmd, context):
    # replace ${ENV_VAR} with os.environ, and {{key}} with context values
    import os
    # first expand environment variables like ${VAR}
    for part in re.findall(r"\$\{([^}]+)\}", cmd):
        val = os.environ.get(part, '')
        cmd = cmd.replace('${' + part + '}', val)
    # then expand simple {{key}} templates from context
    for part in re.findall(r"\{\{([^}]+)\}\}", cmd):
        val = str(context.get(part, '')) if context else ''
        cmd = cmd.replace('{{' + part + '}}', val)
    return cmd

def assert_expected(result_list, exit_code, output):
    results = []
    for assertion in result_list:
        a_type = assertion.get('type')
        if a_type == 'exit_code':
            ok = (exit_code == int(assertion.get('value', 0)))
            results.append({'assertion': assertion, 'ok': ok})
        elif a_type == 'output_non_empty':
            ok = bool(output)
            results.append({'assertion': assertion, 'ok': ok, 'output_sample': output[:200]})
        elif a_type == 'file_exists':
            path = assertion.get('path')
            # special token 'pipeline_yaml' maps to common filenames
            if path == 'pipeline_yaml':
                ok = any(Path(p).exists() for p in ['azure-pipelines.yml', '.github/workflows'])
            else:
                ok = Path(path).exists()
            results.append({'assertion': assertion, 'ok': ok})
        elif a_type == 'contains':
            value = assertion.get('value')
            ok = value in output
            results.append({'assertion': assertion, 'ok': ok, 'output_sample': output[:200]})
        elif a_type == 'regex':
            pattern = assertion.get('pattern')
            ok = False
            if pattern and output:
                ok = re.search(pattern, output) is not None
            results.append({'assertion': assertion, 'ok': ok, 'pattern': pattern})
        elif a_type == 'json_match':
            # simple dot-path extractor
            jp = assertion.get('json_path')
            ok = False
            value = None
            try:
                obj = json.loads(output) if output else None
                if obj and jp:
                    parts = jp.split('.')
                    cur = obj
                    for p in parts:
                        if isinstance(cur, dict) and p in cur:
                            cur = cur[p]
                        else:
                            cur = None
                            break
                    value = cur
                    expected_val = assertion.get('value')
                    if expected_val is None:
                        ok = cur is not None
                    else:
                        ok = cur == expected_val
            except Exception:
                ok = False
            results.append({'assertion': assertion, 'ok': ok, 'json_value': value})
        elif a_type == 'numeric_compare':
            # compare numeric value from json_path or output
            jp = assertion.get('json_path')
            operator = assertion.get('operator')
            threshold = assertion.get('threshold')
            actual = None
            try:
                if jp and output:
                    obj = json.loads(output)
                    parts = jp.split('.')
                    cur = obj
                    for p in parts:
                        if isinstance(cur, dict) and p in cur:
                            cur = cur[p]
                        else:
                            cur = None
                            break
                    actual = cur
                else:
                    # try parse output as number
                    actual = float(output.strip()) if output else None
                ok = False
                if actual is not None:
                    if operator == 'gt': ok = actual > float(threshold)
                    if operator == 'ge': ok = actual >= float(threshold)
                    if operator == 'lt': ok = actual < float(threshold)
                    if operator == 'le': ok = actual <= float(threshold)
                    if operator == 'eq': ok = actual == float(threshold)
                    if operator == 'ne': ok = actual != float(threshold)
            except Exception:
                ok = False
            results.append({'assertion': assertion, 'ok': ok, 'actual': actual, 'threshold': threshold})
        elif a_type == 'templates_present':
            # a simple heuristic: look for 'templates' directory
            ok = Path('templates').exists()
            results.append({'assertion': assertion, 'ok': ok})
        elif a_type == 'manual_check':
            results.append({'assertion': assertion, 'ok': None, 'note': 'manual review required'})
        else:
            results.append({'assertion': assertion, 'ok': None, 'note': f'unsupported assertion type: {a_type}'})
    return results

def run_node_rank(node_id, rank):
    tree = load_skill_tree()
    node = tree['nodes'].get(node_id)
    if not node:
        print(f'Node {node_id} not found')
        return 2
    rank_obj = node['ranks'].get(str(rank))
    if not rank_obj:
        print(f'Rank {rank} not found for node {node_id}')
        return 2

    cmds = rank_obj.get('validation_commands', [])
    expected = rank_obj.get('expected_results', [])
    context = node.get('validation_context', {})

    aggregate = []
    for cmd in cmds:
        if cmd.strip().startswith('#'):
            aggregate.append({'command': cmd, 'exit_code': None, 'output': None, 'note': 'skipped comment'})
            continue
        expanded = expand_template(cmd, context)
        aggregate.append({'command': cmd, 'expanded_command': expanded})
        code, out = run_command(expanded)
        assertions = assert_expected(expected, code, out)
        aggregate.append({'command': cmd, 'exit_code': code, 'output': out, 'assertions': assertions})

    print(json.dumps({'node': node_id, 'rank': rank, 'results': aggregate}, indent=2))
    # return non-zero if any assertion failed
    for a in aggregate:
        for asst in a.get('assertions', []):
            if asst.get('ok') is False:
                return 3
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: run_validation.py <NODE_ID> <RANK>')
        sys.exit(2)
    node_id = sys.argv[1]
    rank = sys.argv[2]
    sys.exit(run_node_rank(node_id, rank))
